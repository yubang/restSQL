# coding:UTF-8


from setuptools import setup, find_packages

setup(
    name='restSQL',
    version='0.0.1',
    description='一个URL映射操作数据库的系统',
    author='yubang',
    author_email='yubang93@gmail.com',
    url='https://github.com/yubang/restSQL',
    packages=find_packages(),
    install_requires=['bottle', 'PyMySQL', 'Werkzeug'],
)
