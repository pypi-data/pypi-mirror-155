# coding:utf-8
# 程序配置项 创建日志输出处理器示例

from MDCLogger import LoggerPrintImpl


logger = LoggerPrintImpl.get_logger(app_name="p202020101_app_server", console_print=True,
                                    log_path="/logs", backup_count=2, when="H")

