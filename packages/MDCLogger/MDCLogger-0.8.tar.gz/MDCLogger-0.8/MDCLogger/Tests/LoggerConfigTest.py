# coding:utf-8
# 日志模块输出单元使用样例


from .LoggerConfig import logger


def do_some_work():
    logger.debug("debug级别日志输出内容样例")
    logger.trace("trace级别日志输出内容样例")
    logger.warn("warn级别日志输出内容样例")
    logger.error("error级别日志输出内容样例")
    logger.info("info级别日志输出内容样例")



@MDCLoggerImpl.with_log_trace()
def support_parent_trace():
    logger.debug("这里已经不是最初的溯源id了==%s", "support_parent_trace")


@MDCLoggerImpl.with_log_trace(False)
def restart_trace():
    logger.debug("这里重新开始了溯源id==%s", "restart_trace")
    support_parent_trace()
    return "我已经脱离了最初的溯源新启动的id=%s" % MDCLoggerImpl.getTraceId()


@MDCLoggerImpl.with_log_trace(support_parent_trace=False)
def trace_test_start():
    logger.debug("这是溯源开始的地方，每次traceid都不会相同==%s", "trace_test_start")
    do_some_work()
    res = restart_trace()
    print(res)


from concurrent.futures import ThreadPoolExecutor
if __name__ == "__main__":
    in_log = JournalLog("2020-09-15 17:26:27", "2020-09-15 17:26:36", "http:test.com", "post")
    logger.internal_log(json_data=in_log.json(), extra={"key_name": "内部流水中其他想打印到日志里的信息"})
    # logger.debug("这个地方和溯源无关，traceid还没有设置,接下来将开启20个线程，来验证单个线程溯源id是相同的")
    # t = ThreadPoolExecutor()
    # for i in range(20):
    #     t.submit(trace_test_start)
    #     time.sleep(20)
    # logger.debug("溯源验证已结束了，trace已再trace_test_start结束时清除了")





