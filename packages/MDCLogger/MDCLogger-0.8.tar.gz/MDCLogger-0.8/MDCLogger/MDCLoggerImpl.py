# coding=UTF-8
# author: zhangzixiao
# email:  zhangzixiao@189.cn

__author__ = 'zhangzixiao'
# The following module attributes are no longer updated.
__version__ = "0.6"
__date__ = "2020.09.08"

import threading
from functools import wraps
import logging
import logging.handlers
import sys, os, socket, time, datetime, uuid
import json

MDC_LOCAL_DATA = threading.local()

# 分5个文件
# app_debug.log 业务日志
# app_info.log 流水日志
# app_warning.log 警告类日志
# app_error.log 异常日志
# app_trace.log 埋点日志
# 需要注意的是 每个类型日志文件中只能输出同级别日志
# 初步实现方式为 每个进程创建五个logger对象分别处理五类日志

# 扩展支持埋点日志级别-同java相同设置级别高于all(0)低于debug(10)
TRACE = 5
TRACE_NAME = "TRACE"
logging.addLevelName(TRACE, TRACE_NAME)
hostname = os.getenv("HOSTNAME", socket.gethostname())
LOG_LEVEL_MODEL = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR"]
TRACEID_NAME = "traceId"


def start_trace(trace_id=None):
    """
    开始日志链路追踪
    :param trace_id:
    :return:
    """
    if not trace_id:
        trace_id = str(uuid.uuid4()).replace('-', '')
    MDC_LOCAL_DATA.__setattr__(TRACEID_NAME, trace_id)


def endTrace():
    """
    结束日志链路追踪
    :return:
    """
    t_id = getTraceId()
    if hasattr(MDC_LOCAL_DATA, TRACEID_NAME):
        MDC_LOCAL_DATA.__delattr__(TRACEID_NAME)
    return t_id


def getTraceId():
    if hasattr(MDC_LOCAL_DATA, TRACEID_NAME):
        return MDC_LOCAL_DATA.__getattribute__(TRACEID_NAME)
    return None


def with_log_trace(support_parent_trace=True):
    """
    开启日志 装饰器
    :param support_parent_trace: 是否继续使用的当前线程中未结束的溯源id. 默认True， 置为False:则创建新溯源id
    :return:
    """
    def start_wrapper(fun):

        @wraps(fun)
        def exec_fun(*args, **kwargs):
            t_id = None if not support_parent_trace else getTraceId()
            # 父节点中无溯源id初始化一个
            if not t_id:
                start_trace(t_id)
            res = fun(*args, **kwargs)
            if not support_parent_trace:
                # 继承来的溯源id 当前方法内不清除
                endTrace()
            return res
        return exec_fun
    return start_wrapper


def get_current_log_time():
    """
    获取日志打印时间
    :return:
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time_str[:-3]


class LoggerPrinter(logging.Logger):
    """
    日志输出实现
    """

    info_log_app_name, app_name = "", ""

    def __init__(self, name, app_name, console_print=False):
        """
        初始化方法
        :param name: 日志对象名
        :param app_name: 应用名
         :param console_print: 是否输出日志到控制台
        """
        logging.Logger.__init__(self, name)
        # 控制台是否输出日志
        self.propagate = console_print
        self.app_name = app_name
        self.info_log_app_name = app_name + "_info"
        if sys.version > "3":
            if TRACE not in logging._levelToName:
                logging.addLevelName(TRACE, TRACE_NAME)
        else:
            if TRACE not in logging._levelNames:
                logging.addLevelName(TRACE, TRACE_NAME)

    def trace(self, msg, *args, **kwargs):
        """
        trace 级别日志输出
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        self._log(TRACE, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        debug级别日志输出
        :param msg: 消息
        :param args:
        :param kwargs:
        :return:
        """
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        info 级别日志输出 注意：此级别日志输出已降级为debug
        :param msg: 描述
        :param args:
        :param kwargs:
        :return:
        """
        if self.isEnabledFor(logging.INFO):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        error级别日志输出
        :param msg: 描述
        :param args:
        :param kwargs:
        :return:
        """
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """
        warning级别日志输出
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        self.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        warning级别日志输出
        :param msg: 描述
        :param args:
        :param kwargs:
        :return:
        """
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, args, **kwargs)

    def external_log(self, json_data, *args, **kwargs):
        """
        外部流水日志输出
        :param json_data
        :param args:
        :param kwargs:
        :return:
        """
        if not isinstance(json_data, dict):
            self.warn("内部流水格式 错误: %s" % str(json_data))
        else:
            if TRACEID_NAME not in json_data:
                json_data[TRACEID_NAME] = getTraceId()
            ex = kwargs.get("extra")
            if ex and isinstance(ex, dict):
                json_data.update(ex)
            find_res = self.findCaller()
            filename = None if len(find_res) < 1 else find_res[0]
            co_name = None if len(find_res) < 2 else find_res[2]
            extra = {"level": "INFO", "log_type": "visit", "dialog_type": "out",
                     "logger":str(filename), "log_time": get_current_log_time(),
                     "funcName": "journalLogInterceptor" if not co_name else str(co_name),
                     "app_name": self.info_log_app_name,
                     }
            json_data.update(extra)
            self._log(logging.INFO, json.dumps(json_data, ensure_ascii=False), args, **kwargs)

    def internal_log(self, json_data, *args, **kwargs):
        """
        内部流水日志输出
        :param json_data: 描述
        :param args:
        :param kwargs:
        :return:
        """

        if not isinstance(json_data, dict):
            self.warn("内部流水格式 错误: %s" % str(json_data))
        else:
            if TRACEID_NAME not in json_data:
                json_data[TRACEID_NAME] = getTraceId()
            ex = kwargs.get("extra")
            if ex and isinstance(ex, dict):
                json_data.update(ex)
            find_res = self.findCaller()
            filename = None if len(find_res) < 1 else find_res[0]
            co_name = None if len(find_res) < 2 else find_res[2]
            # co_filename, f.f_lineno, co.co_name
            # co_filename, f.f_lineno, co.co_name sinfo
            extra = {"level": "INFO", "log_type": "visit", "dialog_type": "in",
                     "logger": str(filename), "log_time": get_current_log_time(),
                     "funcName": "BaseHandle" if not co_name else str(co_name),
                     "app_name": self.info_log_app_name,
                     }
            json_data.update(extra)
            self._log(logging.INFO, json.dumps(json_data, ensure_ascii=False), args, **kwargs)


class LogstashFormatter(logging.Formatter):
    """
    日志内容格式化方法扩展
    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """
    # 日志对象中一些重复项在输出到日志文件中剔除
    record_ignore_keys = ["name", "args", "levelname", "levelno", "pathname", "exc_info", "filename",
                          "exc_text", "stack_info", "msg", "message", 'msecs', 'relativeCreated']
    default_time_format = '%Y-%m-%d %H:%M:%S'
    default_msec_format = '%s.%03d'
    app_name = ""
    level_name = "debug"
    log_type = "desc"
    log_app_name = ""

    # def __init__(self, app_name, level_name="debug", fmt=None, datefmt=None, style='%'):
    #     if style not in logging._STYLES:
    #         raise ValueError('Style must be one of: %s' % ','.join(logging._STYLES.keys()))
    #     self._style = logging._STYLES[style][0](fmt)
    #     self._fmt = self._style._fmt
    #     self.datefmt = datefmt

    def __init__(self, app_name, level_name="debug", log_type="desc"):
        logging.Formatter.__init__(self)
        self.app_name = app_name
        self.level_name = level_name
        self.log_type = log_type
        if str(self.level_name).upper() == "TRACE":
            self.log_app_name = "%s_trace" % self.app_name
        elif str(self.level_name).upper() == "INFO":
            self.log_app_name = "%s_info" % self.app_name
        else:
            self.log_app_name = "%s_code" % self.app_name

    def formatTime(self, record, datefmt=None):

        """
        Return the creation time of the specified LogRecord as formatted text.

        This method should be called from format() by a formatter which
        wants to make use of a formatted time. This method can be overridden
        in formatters to provide for any specific requirement, but the
        basic behaviour is as follows: if datefmt (a string) is specified,
        it is used with time.strftime() to format the creation time of the
        record. Otherwise, an ISO8601-like (or RFC 3339-like) format is used.
        The resulting string is returned. This function uses a user-configurable
        function to convert the creation time to a tuple. By default,
        time.localtime() is used; to change this for a particular formatter
        instance, set the 'converter' attribute to a function with the same
        signature as time.localtime() or time.gmtime(). To change it for all
        formatters, for example if you want all logging times to be shown in GMT,
        set the 'converter' attribute in the Formatter class.
        """
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime(self.default_time_format, ct)
            s = self.default_msec_format % (t, record.msecs)
        return s

    def format(self, record):
        """
        重写模板，删除不需要或重复的key
        """
        fields = record.__dict__.copy()
        log_msg = fields.get("msg")
        if hasattr(record, "getMessage"):
            log_msg = record.getMessage()
        log_time = fields.get("asctime", None)
        if not log_time:
            log_time = get_current_log_time()

        # # app_name:应用系统名称
        # # HOSTNAME:主机ip或者主机名称
        # # logger:发生日志行为的类
        # log_type:日志类型，推荐分类有 /desc/monitor/visit 等
        # level:日志等级
        # log_time:产生日志的时间
        # thread:线程名
        # code_message:信息
        log_data = {"log_time": log_time,
                    "app_name": self.log_app_name,
                    "log_type": self.log_type,
                    "level":  self.level_name,
                    "code_message": log_msg,
                    "traceId": getTraceId(),
                    "logger": fields.get("filename"),
                    "HOSTNAME": hostname
                    }
        for k in fields:
            # 实现将日志中扩展属性extra填充到要输出的日志内容中
            if k not in self.record_ignore_keys:
                log_data[k] = fields.get(k)

        return json.dumps(log_data, ensure_ascii=False)

