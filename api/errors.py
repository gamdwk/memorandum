from flask_restful import abort
from werkzeug.http import HTTP_STATUS_CODES
from flask import make_response, jsonify


class ResponseCode:
    SUCCESS = 200
    WRONG_PARAM = 400
    MESSAGE = '处理成功！'


def generate_response(data=None, message=ResponseCode.MESSAGE, status=ResponseCode.SUCCESS):
    return {
        'status': status,
        'message': message,
        'data': data
    }


def api_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        abort(400, **generate_response(data=kwargs.get('message'), message='参数错误！', status=http_status_code))
    if http_status_code == 401:
        abort(401, **generate_response(data=[kwargs.get('message')], message="请认证", status=http_status_code))
    if http_status_code == 403:
        abort(403, **generate_response(data=[kwargs.get('message')], message="资源不可用", status=http_status_code))
    if http_status_code == 404:
        abort(404, **generate_response(data=kwargs.get('message'), message="不存在的URI", status=http_status_code))
    if http_status_code == 405:
        abort(405, **generate_response(data=[kwargs.get('message')], message="错误的方法", status=http_status_code))
    if http_status_code == 500:
        abort(500, **generate_response(data=[kwargs.get('message')], message="内部服务器错误", status=http_status_code))
    return abort(http_status_code)
