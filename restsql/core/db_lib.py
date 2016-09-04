# coding:UTF-8

"""
数据库操作简易封装
@author: yubang
2016.02.29
"""

import pymysql as MySQLdb


class Model:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name

    @staticmethod
    def __print_sql(sql):
        """打印执行的sql"""
        print("执行了sql：", sql)

    def get_db_connection(self):
        """
        获取新的数据库连接，请注意自己关闭连接
        :return:
        """
        conn = MySQLdb.connect(host=self.db_config.db_host, user=self.db_config.db_username,
                               passwd=self.db_config.db_password,
                               db=self.db_config.db_name, port=self.db_config.db_port, charset="utf8")
        return conn

    @staticmethod
    def close_db_connection(db_connection):
        """
        关闭数据库连接
        :param db_connection: 数据库连接句柄
        :return:
        """
        db_connection.close()

    def query_for_dict(self, sql, params=None):
        """
        执行数据库查询，返回一个字典，如果没有数据返回None
        :param sql: 原始sql
        :param params: 需要填充的参数列表（字符串自动转椅）
        :return:
        """
        objs = self.query_for_list(sql, params)
        if objs:
            return objs[0]
        else:
            return None

    def query_for_list(self, sql, params=None):
        """
        执行数据库查询，返回一个列表，如果没有数据返回None
        :param sql: 原始sql
        :param params: 需要填充的参数列表（字符串自动转椅）
        :return:
        """
        conn = self.get_db_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)

        # 记录执行的sql
        self.__print_sql(cursor._executed)

        objs = cursor.fetchall()
        cursor.close()
        self.close_db_connection(conn)
        return objs

    def update(self, sql, params=None):
        """
        执行sql，返回影响行数
        :param sql: 原始sql
        :param params: 需要填充的参数列表（字符串自动转椅）
        :return:
        """
        if params is None:
            params = []
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)

        # 记录执行的sql
        self.__print_sql(cursor._executed)

        count = cursor.rowcount
        conn.commit()
        cursor.close()
        self.close_db_connection(conn)
        return count

    def insert(self, sql, params):
        """
        执行sql，返回插入后自增id
        :param sql: 原始sql
        :param params: 需要填充的参数列表（字符串自动转椅）
        :return:
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)

        # 记录执行的sql
        self.__print_sql(cursor._executed)

        table_id = int(cursor.lastrowid)
        conn.commit()
        cursor.close()
        self.close_db_connection(conn)
        return table_id
