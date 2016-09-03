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
