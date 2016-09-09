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
from restsql.core.power import PowerManager
import re
import json


class BaseApp:
    def __init__(self, wsgi_app=None):
        self.wsgi = self.__main
        self.__model_dict = {}
        self.db_config = None
        self.__other_wsgi = self.__default_other_wsgi if not wsgi_app else wsgi_app
        self.__handler_prefix_url = '/'
        self.__power = {}

    def __call__(self, environ, start_response):
        return self.__main(environ, start_response)

    @staticmethod
    def __default_other_wsgi(environ, start_response):
        """默认的第三方处理"""
        r = Response("Not Found!", 404)
        return r(environ, start_response)

    def __check_user_other_framework(self, url):
        """检查是否使用第三方框架处理"""
        return not url.startswith(self.__handler_prefix_url)

    def __main(self, environ, start_response):
        """wsgi入口函数"""
        request = Request(environ)

        # 判断是否使用第三方框架处理
        if self.__check_user_other_framework(request.path):
            return self.__other_wsgi(environ, start_response)

        r = self.__handler(request)
        r.headers['server'] = 'resetSQL'
        return r(environ, start_response)

    @staticmethod
    def __make_response(code, msg, content, status_code=200):
        """制作response对象"""
        if content:
            r = Response(json.dumps(content, cls=JsonEncoder), mimetype="application/json")
        else:
            r = Response("{}", mimetype="application/json")
        r.status_code = status_code
        return r

    def __handler(self, request):
        """各种http请求类型分发处理"""
        q = QueryModelMap(request, re.sub('^'+self.__handler_prefix_url, '', request.path))

        # 检查权限
        Power = self.__power.get(q.model_name, PowerManager)
        power = Power(request)
        if not power.check_power():
            return Response("forbidden!", status=403, mimetype='text/plain')

        # 出现解析错误
        if q.code != 0:
            return self.__make_response(q.code, q.msg, None)

        # 判断模型是否存在
        model_name = self.__model_dict.get(q.model_name, None)
        if not model_name:
            return Response('not found!', status=404, mimetype='text/plain')

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

    def set_rest_sql_handler_prefix_url(self, prefix_url):
        """
        设置restSQL处理的前缀
        :param prefix_url: 处理前缀
        :return:
        """
        self.__handler_prefix_url = prefix_url

    def set_other_wsgi(self, wsgi):
        """设置第三方wsgi处理接口"""
        self.__other_wsgi = wsgi

    def set_power_manager(self, power_manager_dict):
        """
        设置权限管理
        :param power_manager_dict: 模型权限管理映射字典
        :return:
        """
        self.__power = power_manager_dict
