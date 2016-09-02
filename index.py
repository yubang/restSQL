# coding:UTF-8


"""
restSQL小系统入口文件
@author: yubang
"""


from core.app import app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8000, app, use_debugger=True, use_reloader=True)
