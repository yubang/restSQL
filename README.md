# restSQL
### restSQL是一个基于python实现的将数据库转换为 REST 风格的 Web 服务

创作该项目源自于看了美团的一篇博客 [http://tech.meituan.com/koa-restql.html](http://tech.meituan.com/koa-restql.html) ,但是美团给出的是基于node的实现版本，所以使用python来实现该功能。

### 项目开发环境

 1. 基于python3.5，不兼容python2
 2. 基于Werkzeug
 3. 暂时只支持mysql

### 第一个hello world！

请查看index.py的代码，就是那么简单


### API说明

1. 数据库查询操作

| HTTP请求方法 | 请求的URL | 返回值 |功能 | 备注 |
| --- | --- | --- | --- |
| GET | /<模型别名>/<主键ID> | 字典 |查询主键id为XXX的一条数据| GET参数是where条件 |
| GET | /<模型别名> | 数组 | 查询所有符合条件的数据| GET参数是where条件 |

2. 数据库插入操作

| HTTP请求方法 | 请求的URL | 返回值 |功能 | 备注 |
| --- | --- | --- | --- |
| POST | /<模型别名> | 空字典，状态码返回201 |创建一条新数据| GET参数是where条件 |

### 其它操作正在按开发规范修正接口
### 权限控制模块正在开发中
### 与别的python web框架结合功能正在开发中
