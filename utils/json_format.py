# -*- coding: utf-8 -*-
import json
from bson import objectid
from decimal import Decimal
import datetime


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, objectid.ObjectId):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def jsonfy_rpt(data):
    return json.dumps(data, cls=CJsonEncoder)


def jsonify_data(data):
    return json.dumps(data, cls=CJsonEncoder)