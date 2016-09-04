# coding:UTF-8


"""
restSQL小系统入口文件
@author: yubang
"""

from restsql.core.app import BaseApp


class Config:
    """mysql配置"""
    db_name = 'test'
    db_host = '127.0.0.1'
    db_port = 3306
    db_username = 'root'
    db_password = ''


app = BaseApp()
# 表名和模型名字映射，第一个是模型名字
app.update_model({"user": 'user'})
# 配置数据库信息
app.set_db_config(Config())

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('0.0.0.0', 8000, app.wsgi, use_debugger=True, use_reloader=True)
