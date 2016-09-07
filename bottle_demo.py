# coding:UTF-8


"""
与其它WEB框架结合的小例子
@author: yubang
"""

from bottle import Bottle, run
from restsql.core.app import BaseApp

app = Bottle()

class Config:
    """mysql配置"""
    db_name = 'test'
    db_host = '127.0.0.1'
    db_port = 3306
    db_username = 'root'
    db_password = ''


@app.get('/debug')
def index():
    return "debug!"

if __name__ == '__main__':
    base_app = BaseApp(app) # 把别的框架的wsgi接口作为构造函数就好
    base_app.set_db_config(Config())
    base_app.update_model({"user_model": 'user'})
    base_app.set_rest_sql_handler_prefix_url('/restSQL') # 设置要给restSQL处理的URL地址前缀
    run(base_app, port=8000)
