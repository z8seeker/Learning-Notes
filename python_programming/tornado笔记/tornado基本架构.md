# 基本架构

tornado 是一个典型的 `prefork + io event loop` 的 web server 架构，tornado 的架构是很简单清晰的：

- ioloop 是 tornado 的核心，它就是一个 `io event loop`，底层封装了 `select`，`epoll`和 `kqueue`，并根据不同的平台选择不同的实现。
- iostream 封装了 `non-blocking socket`，用它来进行实际 socket 的数据读写。
- TCPServer 则是通过封装 ioloop 实现了一个简易的 server，同时我们也在这里进行 prefork 的处理
- HTTPServer 则是继承 TCPServer 实现了一个能够处理 http 协议的 server。
- Application 则是实际处理 http 请求的模块，HTTPServer 收到 http 请求并解析之后会通过 Application 进行处理。
- `RequestHandler` 和 `WebSocketHandler` 则是注册给 Application 用来处理对应 url 的。
- `WSGIApplication` 则是 tornado 用于支持 WSGI 标准的接口，通过 `WSGIContainer` 包装供 HTTPServer 使用。


## Tornado 模块分类


### 1. Asynchronous networking 底层模块
 
tornado.ioloop — 核心的 I/O 循环
tornado.iostream — 对非阻塞式的 socket 的简单封装，以方便常用读写操作
tornado.httpclient — 一个非阻塞的HTTP 客户端实现
tornado.netutil — 一些网络应用的实现，主要实现 TCPServer 类

### 2. Core web framework

tornado.web — 包含 web 框架的大部分主要功能，包含 RequestHandler 和 Application 两个重要的类
tornado.httpserver — 一个非阻塞 HTTP 服务器的实现
tornado.template — 模版系统
tornado.escape — HTML,JSON,URL 等的编码解码和一些字符串操作
tornado.locale — 国际化支持

### 3. Integration with other services

tornado.auth — 使用 OpenId 和 OAuth 进行第三方登录
tornado.database — 简单的 MySQL 服务端封装
tornado.platform.twisted — 在 Tornado 上运行为 Twisted 实现的代码
tornado.websocket — 实现和浏览器的双向通信
tornado.wsgi — 与其他 python 网络框架/服务器的相互操作

### 4. Utilities

tornado.autoreload — 生产环境中自动检查代码更新
tornado.gen — 一个基于生成器的接口，使用该模块保证代码异步运行
tornado.httputil — 分析 HTTP 请求内容
tornado.options — 解析终端参数
tornado.process — 多进程实现的封装
tornado.stack_context — 用于异步环境中对回调函数的上下文保存、异常处理
tornado.testing — 单元测试


待续 http://www.nowamagic.net/academy/detail/13321017