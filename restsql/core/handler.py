# coding:UTF-8


"""
数据库操作封装处理
@author: yubang
"""


from restsql.core import error_code
import traceback


class Handler:

    @classmethod
    def query(cls, query_mode_map, model):
        """
        执行数据库查询
        :param query_mode_map: restsql.core.query.QueryModelMap 对象
        :param model: 模型对象
        :return:
        """

        sql = "select * from " + model.table_name + " WHERE " + query_mode_map.where

        try:
            if query_mode_map.command == 'one':
                data = model.query_for_dict(sql + " limit 1;", query_mode_map.where_value)
            elif query_mode_map.command == 'some':
                data = model.query_for_list(sql, query_mode_map.where_value)
            else:
                data = model.query_for_list(sql, query_mode_map.where_value)
        except Exception:
            traceback.print_exc()
            return error_code.DB_ERROR[0], error_code.DB_ERROR[1], None
        return 0, "ok", data

    @classmethod
    def insert_into(cls, query_mode_map, model):
        """
        执行数据库插入
        :param query_mode_map: restsql.core.query.QueryModelMap 对象
        :param model: 模型对象
        :return:
        """
        sql = "insert into " + model.table_name + query_mode_map.insert
        try:
            r = model.insert(sql, query_mode_map.insert_value)
            sql = "select * from " + model.table_name + " where id = %s limit 1;"
            r = model.query_for_dict(sql, [r])
        except Exception:
            traceback.print_exc()
            return error_code.DB_ERROR[0], error_code.DB_ERROR[1], None
        return 0, "ok", r

    @classmethod
    def update(cls, query_mode_map, model):
        """
        执行数据库更新
        :param query_mode_map: restsql.core.query.QueryModelMap 对象
        :param model: 模型对象
        :return:
        """
        sql = "update " + model.table_name + " SET " + query_mode_map.update
        if query_mode_map.command == 'update one':
            sql += ' limit 1;'
        try:
            query_mode_map.command = "one" if query_mode_map.command == 'update one' else 'all'
            r = cls.query(query_mode_map, model)[2]
            model.update(sql, query_mode_map.update_value)
        except Exception:
            traceback.print_exc()
            return error_code.DB_ERROR[0], error_code.DB_ERROR[1], None
        return 0, "ok", r

    @classmethod
    def delete(cls, query_mode_map, model):
        """
        执行数据库删除
        :param query_mode_map: restsql.core.query.QueryModelMap 对象
        :param model: 模型对象
        :return:
        """
        sql = "delete from " + model.table_name + " WHERE " + query_mode_map.where
        if query_mode_map.command == 'delete one':
            sql += ' limit 1;'
        try:
            r = model.update(sql, query_mode_map.where_value)
        except Exception:
            traceback.print_exc()
            return error_code.DB_ERROR[0], error_code.DB_ERROR[1], None
        return 0, "ok", r
