from rest_framework.response import Response

from fairyspace.core.exception import ERROR_PHRASES


def success_response(data=None):
    """成功返回的数据结构

    {
        'code': 0,
        'message': '',
        'result': data,
    }
    """

    return Response({'code': 0, 'message': '', 'result': data})


def error_response(code, message=None, data=None, app=None):
    """业务异常返回的数据结构，这里返回了四种数据结构

    code:     错误码
    message:  错误提示消息
    data:     返回的错误的数据
    app:      指定是哪个 app 出了问题，以方便定位问题

    {
        'code': code,
        'message': message,
        'data': data,
        'app': app,
    }
    """

    if message is None:
        message = ERROR_PHRASES.get(code, '')

    response_data = {
        'code': code,
        'message': message,
        'data': data,
        'app': app,
    }

    return Response(response_data)
