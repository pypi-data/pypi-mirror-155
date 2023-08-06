# coding: utf-8


class JournalLog:
    """
    内/外部流水日志对象 约定参数模型
    """
    __slots__ = ['transaction_id',  # 流水id
                 'dialog_type',  # in/out 内部流水日志/外部流水日志
                 'request_time',  # 请求时间(时间格式yyyy-MM-dd HH:mm:ss.SSS)
                 'response_time',  # 响应时间(时间格式yyyy-MM-dd HH:mm:ss.SSS)
                 'address',  # 请求访问地址
                 'http_method',  # 请求方式
                 'key_type',  # 核心关键参数类型()
                 'key_param',  # 核心关键参数(比如order_id)
                 'request_payload',  # 请求参数
                 'response_payload',  # 响应参数
                 'request_headers',  # 头部信息
                 'response_headers',  # 头部信息
                 'response_code',  # 业务级响应码（错误码）。
                 'response_remark',  # 业务级响应描述文字。
                 'http_status_code',  # HTTP状态码（常见的状态码：200-服务器成功返回网页，404–请求的网页不存在，503–服务不可用等）
                 'total_time',  # 接口处理总耗时
                 'fcode',  # 调用方编码,
                 'tcode',  # 被调用方编码
                 'method_code',  # 接口方法编码, 参考：新架构平台编码规范method
                 ]

    def __init__(self,
                 request_time,  # 请求时间(时间格式yyyy-MM-dd HH:mm:ss.SSS)
                 response_time,  # 响应时间(时间格式yyyy-MM-dd HH:mm:ss.SSS)
                 address,  # 请求访问地址
                 http_method,  # 请求方式
                 dialog_type="in",  # in/out 内部流水日志/外部流水日志
                 request_payload='',  # 请求参数
                 response_payload='',  # 响应参数
                 request_headers='',  # 头部信息
                 response_headers='',  # 头部信息
                 response_code='',  # 业务级响应码（错误码）。
                 response_remark='',  # 业务级响应描述文字。
                 http_status_code='',  # HTTP状态码（常见的状态码：200-服务器成功返回网页，404–请求的网页不存在，503–服务不可用等）
                 total_time=0,  # 接口处理总耗时
                 method_code='',  # 接口方法编码, 参考：新架构平台编码规范method
                 transaction_id='',  # 流水id
                 key_type='String',  # 核心关键参数类型(详见S_DIC.KEY_TYPE)
                 key_param='transaction_id',  # 核心关键参数(比如order_id)
                 fcode='',  # 调用方编码, 参考：新架构平台编码规范f_code
                 tcode=''  # 被调用方编码, 参考：新架构平台编码规范t_code
                 ):
        self.dialog_type = dialog_type
        self.request_time = request_time
        self.response_time = response_time
        self.address = address
        self.http_method = http_method
        self.request_payload = request_payload
        self.response_payload = response_payload
        self.request_headers = request_headers
        self.response_headers = response_headers
        self.response_code = response_code
        self.response_remark = response_remark
        self.http_status_code = http_status_code
        self.total_time = total_time
        self.method_code = method_code
        self.transaction_id = transaction_id
        self.key_type = key_type
        self.key_param = key_param
        self.fcode = fcode
        self.tcode = tcode

    def json(self):
        return {
            "dialog_type": self.dialog_type,
            "request_time": self.request_time,
            "response_time": self.response_time,
            "address": self.address,
            "http_method": self.http_method,
            "request_payload": self.request_payload,
            "response_payload": self.response_payload,
            "request_headers": self.request_headers,
            "response_headers": self.response_headers,
            "response_code": self.response_code,
            "response_remark": self.response_remark,
            "http_status_code": self.http_status_code,
            "total_time": self.total_time,
            "method_code": self.method_code,
            "transaction_id": self.transaction_id,
            "key_type": self.key_type,
            "key_param": self.key_param,
            "fcode": self.fcode,
            "tcode": self.tcode
        }
