[TOC]

## 应用配置
使用psotgresql数据库，flask框架，sqlalchemy做orm，gunicorn启动
其中sqlalchemy版本为0.8.2，使用了flask-sqlalchemy做扩展

## 错误排查
1. 首先再次访问出错url，错误并未复现；但隔段时间又会出现该错误，而且问题出现位置并不一致。由此可以推断此错误与代码逻辑并没有关系。

2. 连接问题，就需要看看是客户端连接的问题还是服务端出的问题；
首先看看服务端由于没有查看psql数据库日志的权限，所以写了一个脚本，每隔1s向数据库插入数据，然后看看在出现错误的时候插入的数据是否正常。代码大概如下：

	```python
	# -*- coding: utf-8 -*-

	import time
	from os import environ

	import psycopg2

	PG_DBNAME = environ.get('PG_DBNAME', 'stress')
	PG_USER = environ.get('PG_USER', 'stress')
	PG_PASSWORD = environ.get('PG_PASSWORD', 'ssss')
	PG_HOST = environ.get('PG_HOST', '127.0.0.1')
	PG_PORT = environ.get('PG_PORT', 5432)

	conn = psycopg2.connect(
		dbname=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)

	cur = conn.cursor()

	if __name__ == '__main__':
		while True:
			cur.execute('insert into healthz default values;')
			conn.commit()
			time.sleep(1)

	```
事实证明，在sentry再次报错的时候，服务端运行正常，可见出问题的是客户端，即sqlalchemy连接池的问题。

## 错误解决
使用的sqlalchemy来连接psql数据库，所以问题大概率出在sqlalchemy连接池上。
### 解决方式
查看sqlalchemy[官方文档](https://docs.sqlalchemy.org/en/13/core/pooling.html)，官方针对断开连接的问题提供了乐观处理和悲观处理两种方式，目前用了悲观处理的方式。

悲观处理也有两种方式，一种是直接使用官方参数poll_pre_ping，另一种则是自定义解决方法，官网提供了示例文档：

```python
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

some_engine = create_engine(...)

@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result
```

### 解决原理
SQLAlchemy 自身提供了连接池 poll 来管理所有和 database 的连接，工作流程如下：
[![](http://static.git-star.com/a0b501e5016ede9ad1ff0a2bb23036a0.jpg)](http://static.git-star.com/a0b501e5016ede9ad1ff0a2bb23036a0.jpg)

从 pool 中获取新的连接，如果没有就创建一个新的连接并返回，在调用连接的 close 之后，连接不会真正的关闭而是返回 pool 供下次使用，是一种复用连接的机制。

为了保证连接池里的连接的可用性，在每次获取新的 connection 供 application 使用之前，都在 connection 上进行一个简单的测试，比如发送一条简单的 select 1 语句以测试当前 database 是否可用，这就是SQLAlchemy的悲观处理机制，如果预检测发现 connection 不可用，当前 connection 会立马被回收，而且在 pool 中创建时间小于当前 connection 的所有 connection 都会被回收。


### 实际应用
由于应用的sqlalchemy版本较老，为0.8.2；而poll_pre_ping参数是sqlalchemy1.2版本才有的特性，engine_connect事件也是0.9.0才有的事件；所以横竖都是要升级sqlalchemy的，于是两种方式都试用了一下。

老应用使用了flask-sqlalchemy，所以需要做一下兼容修改，大概修改方式如下：

```python
# 针对poll_pre_ping
# 重载apply_driver_hacks函数
class SQLiteAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update({
            'pool_pre_ping': True,
        })
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)

db = SQLiteAlchemy(app)
```

### 后续杂谈
从0.8.2升级到0.9.0和1.2.0都遇到了一些坑，花费了很多时间去处理，在此做一下记录。


1. 0.8升级到0.9，如果代码里使用了from __future__ import unicode_literals；会出现too many values to unpack的问题；
这是因为sqlalchemy在isinstance判断的时候出了问题，后续在1.0版本里做了[修复](https://github.com/sqlalchemy/sqlalchemy/commit/6d3e563a575bcdc57c966980abc5038337505566)

2. 0.8升级到1.2，在使用hybrid_property的时候，需要确保hybrid_property装饰的函数名与setter装饰的函数名保持一致；

	```python
	@hybrid_property
	def admin_title(self):
		pass

	@admin_title.setter
	def admin_title(self, value):
		pass
	```
	否则会报hybrid_property can't set attribute的错误'

3. 0.8升级到1.2，在order by joinedload的model的字段时，需要join一下对应的表，不然会有 invalid reference to FROM-clause entry for table 的问题；
具体描述可以看看stackoverflow上的这个[问题](https://stackoverflow.com/questions/34628248/invalid-reference-to-table-while-order-by-applied)

4. 0.8升级到1.2，wtform-sqlalchemy低版本不兼容问题；使用了QuerySelectField的都会有问题；
修复方法可以看看github上的一个[PR](https://github.com/wtforms/wtforms-sqlalchemy/pull/10/commits/b48288393eb55a5f9ea285f549a10053d21ccba3)

5. 0.8升级到1.2，目测sqlahcmey会做全局检查，主站以前有个model的relationship使用了lazy='join'，没升级前一直没有发现这个错误，升级后部署应用的时候会直接报错，也是找了很久才发现这个坑。