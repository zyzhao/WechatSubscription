# -*- coding: utf-8 -*-
from functools import wraps
import json
import utils.date_helper as date_helper
from utils.json_format import CJsonEncoder
from api import *


def response_json(func):
    """
    Decorator: 返回JSON规范化
    Content-Type=application/json
    charset=utf-8
    :param func: 输入函数
    :return:
    """

    @wraps(func)
    def set_response(*args, **kwargs):
        res = func(*args, **kwargs)
        if type(res) is not dict:
            return res
        else:
            return Response(json.dumps(res, cls=CJsonEncoder),
                            content_type="application/json; charset=utf-8")
    return set_response
