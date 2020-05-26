# tornado 简介

tornaod 是一个 python 网络框架和异步的网络库。tornado 通过使用非阻塞的网络 I/O，可以同时打开数以万计的连接，非常适合用于长轮询，websockets 和其他需要为每个用户保持长连接的应用。

## Threads 和 WSGI

Tornado 与大多数 Python 框架不同，其并不是基于 WSGI 的，通常情况下一个进程里只会跑一个线程。

虽然 tornado 在 `tornado.wsgi` 模块里为 WSGI 提供了有限的支持，但这并不是开发的核心关注点，开发的应用应该直接使用 tornado 自己的接口（`tornado.web`）而不是用 WSGI。

一般情况下，tornado 程序不是线程安全的。tornado 中唯一线程安全的方法是 `IOLoop.add_callback`，可以安全的从其他线程进行调用。

我们还可以使用 `IOLoop.run_in_executor` 从另一个线程中异步的运行一个阻塞的函数（blocking function），需要注意的是传入 `run_in_executor` 的函数应该避免引用任何 tornado 对象。使用 `run_in_executor` 与阻塞代码进行交互是 tornado 推荐的方式。
