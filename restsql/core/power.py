# coding:UTF-8


"""
权限管理模块
@author: yubang
"""


class PowerManager:

    def __init__(self, request):
        """构造函数"""
        self.headers = request.headers

    def check_power(self):
        """检查是否有访问权限"""
        return True

    def init(self):
        """访问初始化执行"""
        pass

    def finally_execute(self):
        """访问结束后处理"""
        pass
