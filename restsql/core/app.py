# coding:UTF-8


"""
请求核心处理类
@author: yubang
"""

from werkzeug.wrappers import Request, Response
from restsql.core.query import QueryModelMap
from restsql.core import error_code
from restsql.core.handler import Handler
from restsql.core.db_lib import Model
from restsql.core.json_encoder import JsonEncoder
# from datetime import datetime
import json


class BaseApp:
    def __init__(self):
        self.wsgi = self.__main
        self.__model_dict = {}
        self.db_config = None

    def __main(self, environ, start_response):
        """wsgi入口函数"""
        request = Request(environ)
        r = self.__handler(request)
        r.headers['server'] = 'resetSQL'
        return r(environ, start_response)

    @staticmethod
    def __make_response(code, msg, content, status_code=200):
        """制作response对象"""
        # return Response(json.dumps({"code": code, "msg": msg, "content": content, "time": datetime.now()}, cls=JsonEncoder), 200, mimetype='application/json')
        if content:
            r = Response(json.dumps(content, cls=JsonEncoder), mimetype="application/json")
        else:
            r = Response("{}", mimetype="application/json")
        r.status_code = status_code
        return r

    def __handler(self, request):
        """各种http请求类型分发处理"""
        q = QueryModelMap(request)

        # 出现解析错误
        if q.code != 0:
            return self.__make_response(q.code, q.msg, None)

        # 判断模型是否存在
        model_name = self.__model_dict.get(q.model_name, None)
        if not model_name:
            return self.__make_response(error_code.MODEL_NAME_ERROR[0], error_code.MODEL_NAME_ERROR[1], None)

        model = Model(self.db_config, model_name)
        if request.method == 'GET':
            r = Handler.query(q, model)
            return self.__make_response(r[0], r[1], r[2])
        elif request.method == 'POST':
            r = Handler.insert_into(q, model)
            return self.__make_response(r[0], r[1], r[2], status_code=201)
        elif request.method == 'DELETE':
            r = Handler.delete(q, model)
            return self.__make_response(r[0], r[1], r[2], status_code=204)
        elif request.method == 'PUT':
            r = Handler.update(q, model)
            return self.__make_response(r[0], r[1], r[2])
        else:
            return Response('Method not allowed', 405)

    def update_model(self, model_dict):
        """
        设置模型
        :param model_dict: peewee模型类字典
        :return:
        """
        self.__model_dict = model_dict

    def set_db_config(self, db_config):
        """
        设置数据库配置
        :param db_config:
        :return:
        """
        self.db_config = db_config
