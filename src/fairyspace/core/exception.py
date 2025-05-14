"""
异常错误码，错误消息，通用异常类
"""

# 错误码
FAIRY_INNER_SYSTEM_ERROR = 10000
FAIRY_PARAMETER_FORMAT_ERROR = 10001
FAIRY_PARAMETER_BUSINESS_ERROR = 10002
FAIRY_SERVER_IS_BUSY = 10003
FAIRY_REQUEST_FORBIDDEN = 10004
FAIRY_OBJECT_NOT_FOUND = 10005
FAIRY_APP_LABEL_IS_INVALID = 10006
FAIRY_MODEL_SLUG_IS_INVALID = 10007
FAIRY_CANT_NOT_FIND_MODEL = 10008
FAIRY_BATCH_ACTION_HAND_ERROR = 10009
FAIRY_FUNCTION_NOT_FOUNT = 10010

# 默认的错误消息
FAIRY_GLOBAL_ERROR_MESSAGE = '系统内部处理异常'

# 错误消息
ERROR_PHRASES = {
    FAIRY_INNER_SYSTEM_ERROR: FAIRY_GLOBAL_ERROR_MESSAGE,
    FAIRY_PARAMETER_FORMAT_ERROR: '参数格式错误',
    FAIRY_PARAMETER_BUSINESS_ERROR: '参数业务错误',
    FAIRY_SERVER_IS_BUSY: '服务器繁忙，请稍后再试',
    FAIRY_REQUEST_FORBIDDEN: '您没有执行该操作的权限',
    FAIRY_OBJECT_NOT_FOUND: '找不到对应的数据',
    FAIRY_APP_LABEL_IS_INVALID: '路由中指定的应用标识不合法',
    FAIRY_MODEL_SLUG_IS_INVALID: '路由中指定的模型标识不合法',
    FAIRY_CANT_NOT_FIND_MODEL: '找不到指定的模型',
    FAIRY_BATCH_ACTION_HAND_ERROR: '批量操作执行异常',
    FAIRY_FUNCTION_NOT_FOUNT: '找不到对应的函数处理器',
}


class FairySpaceException(Exception):
    """通用业务异常类"""

    # 对开发人员友好的详尽的异常报错信息
    default_error_data = ''

    # 异常出错的应用标识
    default_error_app = 'fairyspace'

    def __init__(self, error_code=None, error_message=None, error_data=None, error_app=None):

        self.error_code = error_code if error_code is not None else FAIRY_INNER_SYSTEM_ERROR

        if error_message is not None:
            self.error_message = error_message
        else:
            _error_message = ''
            if error_code in ERROR_PHRASES:
                _error_message = ERROR_PHRASES.get(error_code)

            # 如果错误消息为空，则使用默认的错误消息
            if not _error_message:
                _error_message = FAIRY_GLOBAL_ERROR_MESSAGE
            self.error_message = _error_message

        self.error_data = error_data if error_data is not None else self.default_error_data
        self.error_app = error_app if error_app is not None else self.default_error_app

    def __str__(self):
        return f'{self.error_code}-{self.error_app}:{self.error_message},{self.error_data}'
