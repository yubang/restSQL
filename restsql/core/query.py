# coding:UTF-8


"""
模型映射对象封装
@author: yubang
"""


from restsql.core import error_code


class QueryModelMap:
    def __init__(self, request, api_url):

        self.code = 0
        self.msg = 'ok'

        self.model_name = None
        self.command = None
        self.where = "1"
        self.where_value = []
        self.insert = None
        self.insert_value = None
        self.update = None
        self.update_value = None

        self.__url_path = api_url if api_url.startswith('/') else '/' + api_url
        self.__get_args = request.query_string.decode("UTF-8")
        self.__form_args = request.form.copy()
        self.__method = request.method

        self.__handle_args()
        self.__handle_filter()
        self.__handler_form_args()

    def __handle_args(self):
        """
        处理请求参数
        :return:
        """
        arrs = self.__url_path.split("/")
        length = len(arrs)

        # 检查URL参数是否充足
        if length < 2:
            self.code, self.msg = error_code.URL_ERROR
            return

        # 提取模型名字
        self.model_name = arrs[1]

        # 提取操作指令
        if length < 3:
            self.command = 'all'
        elif arrs[2].isdigit():
            self.command = 'one'
            self.__get_args = '&'.join([self.__get_args, "id=" + arrs[2]])
        elif arrs[2] in ['all', 'some', 'one']:
            self.command = arrs[2]
        else:
            self.command = 'all'

        if self.__method == 'POST':
            self.command = 'insert' if self.command != 'one' else "insert one"
        elif self.__method == 'PUT':
            self.command = 'update' if self.command != 'one' else "update one"
        elif self.__method == 'DELETE':
            self.command = 'delete' if self.command != 'one' else "delete one"

    def __handle_filter(self):
        """
        处理where条件
        :return:
        """
        arrs = self.__get_args.split("&")
        if not self.__get_args:
            return

        where = {}
        for arr in arrs:
            t = arr.split("=")
            if len(t) != 2:
                continue
            where[t[0]] = t[1]
        keys = where.keys()
        self.where_value = [where[k] for k in keys]
        where = ["%s=%s" % (k, "%s") for k in keys]
        self.where = ' AND '.join(where)

    def __handler_form_args(self):
        """
        处理在body里面的参数
        :return:
        """
        keys = [k for k in self.__form_args]
        # "() values()"
        self.insert = "(" + ','.join(keys) + ") values(" + ','.join(["%s" for _ in self.__form_args]) + ")"
        self.insert_value = [self.__form_args[k] for k in self.__form_args]

        keys = ["%s = %s" % (k, "%s") for k in self.__form_args]
        self.update = ','.join(keys)
        self.update_value = self.insert_value
