# coding=UTF-8
__author__ = 'zhangzixiao'

# author: zhangzixiao
# email:  zhangzixiao@189.cn
# log 日志输出工具实现
import logging
import logging.handlers
import re
import os
import socket
from MDCLogger import MDCLoggerImpl

# 分5个文件
# app_debug.log 业务日志
# app_info.log 流水日志
# app_warning.log 警告类日志
# app_error.log 异常日志
# app_trace.log 埋点日志
# 需要注意的是 每个类型日志文件中只能输出同级别日志
# 初步实现方式为 每个进程创建五个logger对象分别处理五类日志
# 扩展支持埋点日志级别-同java相同设置级别高于all(0)低于debug(10)

host_name = os.getenv("HOSTNAME", socket.gethostname())

# INFO 级别流水日志格式 格式内容按照流水日志采集规范要求由输出方法定义
info_format = logging.Formatter('%(message)s')

log_dict = dict()


def get_logger(app_name, console_print=False, reset_error_logs=None, log_path="", backup_count=15,
               when="D", log_level_list=None):
    """

    获取 logger 输出对象
    此方法获取的logger对象会返回五个对应的日志输出handle，其对应日志文件路径为：
    host_name= 环境变量中的HOSTNAME 如果取不到则为socket.gethostname()
    trace: <log_path>/<app_name>_pid_trace.log
    debug: <log_path>/<app_name>_pid_debug.log
    info:  <log_path>/<app_name>_pid_info.log
    warn:  <log_path>/<app_name>_pid_warn.log
    error: <log_path>/<app_name>_pid_error.log

     #摘自TimedRotatingFileHandler原码: a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        #  W{0-6} - roll over on a certain day; 0 - Monday
        # Case of the 'when' specifier is not important; lower or upper case  will work.
    :param app_name: 应用名
    :param console_print: 是否控制台输出
    :param reset_error_logs: 需要重置的日志
    :param log_path: 日志根路径
    :param backup_count: 备份文件数
    :param when: 默认为天
    :param log_level_list:
    :return:
    """
    logger_name = "%s_p%s" % (app_name, os.getpid())
    log_t = log_dict.get(logger_name)
    if log_t:
        return log_t

    if log_path and not os.path.exists(log_path):
        os.makedirs(log_path)
    # 代码级别日志格式 区别在于app_name 按照新采集规则设置
    code_log_fmt = """{"app_name": "%s_code", "log_type": "desc", "level": "%s", "log_time": "%s", 
    "HOSTNAME": "%s", "code_message": "%s" }"""
    code_log_fmt = code_log_fmt % (app_name, "%(levelname)s", "%(asctime)s", host_name, "%(message)s")
    code_log_fmt = code_log_fmt.replace("\r", "").replace("\n", "").replace("  ", "")
    logging.basicConfig(format=code_log_fmt, datefmt='%Y-%m-%d %H:%M:%S')

    log_t = MDCLoggerImpl.LoggerPrinter(logger_name, app_name, console_print)
    # 设置日志输出等级为 埋点日志级别(最低级别日志)
    print_levels = None
    if log_level_list and len(log_level_list) > 0:
        print_levels = []
        for log_level in log_level_list:
            up_lev = "NOno" if not log_level else str(log_level).upper()
            if up_lev in MDCLoggerImpl.LOG_LEVEL_MODEL:
                print_levels.append(up_lev)
    if not print_levels or len(print_levels) == 0:
        print_levels = MDCLoggerImpl.LOG_LEVEL_MODEL

    # 是否控制台输出
    if console_print:
        ch = logging.StreamHandler()
        ch.setFormatter(getLoggerFormatter(app_name, "debug"))
        log_t.addHandler(ch)
    error_handle = None
    backup_count = backup_count if backup_count > 0 else 15
    when = "D" if not when else when.upper()
    for level in print_levels:
        handle = get_handle(app_name, level, logger_name, log_path, backup_count, when)
        if not handle:
            continue
        log_t.addHandler(handle)
        if handle.level == logging.ERROR:
            error_handle = handle

    log_dict[logger_name] = log_t
    # 禁用引用依赖的第三方日志输出
    reset_default_log(reset_error_logs, handles=[error_handle], console_print=console_print)

    return log_t


def reset_default_log(log_names, level_def="ERROR", handles=None, console_print=False):
    """
    重置引用依赖日志输出
    :param log_names:
    :param level_def:
    :param handles:
    :param console_print
    :return:
    """
    if log_names:
        for l_n in log_names:
            log = logging.getLogger(l_n)
            log.setLevel(level_def)
            log.propagate = console_print
            log.handlers = handles


def get_handle(app_name, level_name, file_prefix, base_path, backup_count=15, when="D"):
    """
    获取日志输出handle
    :param app_name
    :param level_name
    :param file_prefix
    :param base_path
    :param backup_count
    :param when
    :return:
    """
    level_no = logging._checkLevel(level_name)
    log_path = r'%s/%s_%s.log' % (base_path, file_prefix, level_name.lower())
    handler = logging.handlers.TimedRotatingFileHandler(log_path, when=when, interval=1, backupCount=backup_count)
    reset_log_ext_match(handler)
    handler.setLevel(level_no)
    # 设置过滤等级 只输出同级别日志
    filter = logging.Filter()
    filter.filter = lambda record: record.levelno == level_no
    handler.addFilter(filter)
    # INFO 级别日志格式格式要求按照访问流水日志格式设置 程序自定义输出
    if level_no == logging.INFO:
        handler.setFormatter(info_format)
    elif level_no == MDCLoggerImpl.TRACE:
        # 埋单日志
        handler.setFormatter(getLoggerFormatter(app_name, level_name))
    else:
        # 其他程序日志
        handler.setFormatter(getLoggerFormatter(app_name, level_name))
    return handler


def  reset_log_ext_match(handler):
    """
    重置handler 删除规则中文件后缀的匹配规则
    调整滚动文件的后缀为.log
    调整python2环境中匹配删除文件的正则匹配规则
    :param handler:
    :return:
    """
    handler.suffix = handler.suffix + ".log"
    ext_match = handler.extMatch.pattern
    if ext_match.endswith("\d{2}$"):
        ext_match = ext_match.replace("$", "(\.\w+)?$")
        handler.extMatch = re.compile(ext_match)


def getLoggerFormatter(app_name, level_name):
    return MDCLoggerImpl.LogstashFormatter(app_name, level_name)

