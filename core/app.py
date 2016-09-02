# coding:UTF-8


"""
请求核心处理类
@author: yubang
"""

from werkzeug.wrappers import Request, Response


class BaseApp:
    def init(self, environ, start_response):
        """wsgi入口函数"""
        request = Request(environ)
        r = self.__handler(request)
        r.headers['server'] = 'resetSQL'
        return r(environ, start_response)

    @staticmethod
    def __handler(request):
        """各种http请求类型分发处理"""
        print(request.path)
        if request.method == 'GET':
            return Response('{}', 200, mimetype='application/json')
        elif request.method == 'POST':
            return Response('{}', 200, mimetype='application/json')
        elif request.method == 'DELETE':
            return Response('{}', 200, mimetype='application/json')
        elif request.method == 'PUT':
            return Response('{}', 200, mimetype='application/json')
        else:
            return Response('Method not allowed', 405)

# wsgi对象
app = BaseApp().init
