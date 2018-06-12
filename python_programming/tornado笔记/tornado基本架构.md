# 基本架构

tornado 是一个典型的 `prefork + io event loop` 的 web server 架构，tornado 的架构是很简单清晰的：

- ioloop 是 tornado 的核心，它就是一个 `io event loop`，底层封装了 `select`，`epoll`和 `kqueue`，并根据不同的平台选择不同的实现。
- iostream 封装了 `non-blocking socket`，用它来进行实际 socket 的数据读写。
- TCPServer 则是通过封装 ioloop 实现了一个简易的 server，同时我们也在这里进行 prefork 的处理
- HTTPServer 则是继承 TCPServer 实现了一个能够处理 http 协议的 server。
- Application 则是实际处理 http 请求的模块，HTTPServer 收到 http 请求并解析之后会通过 Application 进行处理。
- `RequestHandler` 和 `WebSocketHandler` 则是注册给 Application 用来处理对应 url 的。
- `WSGIApplication` 则是 tornado 用于支持 WSGI 标准的接口，通过 `WSGIContainer` 包装供 HTTPServer 使用。

