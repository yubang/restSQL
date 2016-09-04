# coding:UTF-8


"""
json通用处理类
@author: yubang
"""


from datetime import datetime, date, time
import json


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (str, int, float, bool, dict, list)):
            return json.JSONEncoder.default(o)
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, time):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(o)

