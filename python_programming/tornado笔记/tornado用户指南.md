# 用户指南

tornado 主要有四个组件：

- 网络框架 （`RequestHandler`）
- HTTP 客户端和服务端实现（`HTTPServer` 和 `AsyncHTTPClient`）
- 异步网络库（`IOLoop` 和 `IOStream`），作为 HTTP 组件的 building blocks，也可以用来实现其他协议
- 协程库（`tornado.gen`），以更加直接的方式编写异步代码，而不是使用回调链

结合使用 tornado 的网络框架和 HTTP server 可以作为 WSGI 的替代方案。虽然可以在一个 WSGI 容器（`WSGIAdapter`）中使用 tornado 的网络框架，或者使用 tornado 的 HTTP Server 作为容器运行其他的 WSGI 框架 （`WSGIContainer`），但都存在一些限制。为了充分发挥 tornado 的性能，需要将 tornado 的框架和 其 HTTP Server 一起使用。


## 异步与非阻塞 I/O

Real-time web features require a long-lived mostly-idle connection per user. 对于传统的同步网络服务器而言，这意味着分别为每一个用户开启一个线程，而这种开销是很昂贵的。

为了最小化并发连接的开销，tornado 使用一个单线程的事件循环。这意味着所有的应用代码应该是异步和非阻塞的，因为单线程中一次只能执行一个操作。

异步与非阻塞是两个紧密相关的概念，也经常互换使用，但需要注意的是，它们其实是不同的东西。

### 阻塞

一个函数在返回前需要等待一些事件发生时就会发生阻塞。一个函数可能因为很多原因发生阻塞：

- 网络 I/O
- 磁盘 I/O
- 互斥锁

实际上，每个函数都会阻塞，只要它正在占用 CPU 运行，至少都会阻塞一段时间。一个极端的需要考虑 CPU 阻塞的例子是当使用 hash 函数进行加密时，将使用几百毫秒的 CPU 时间，这远大于一般的网络连接或读取磁盘的时间。

一个函数可能在一些方面是阻塞的而在另一些方面则是非阻塞的，在 tornado 里讨论阻塞时一般将的是网络 I/O 阻塞。

### 异步

一个异步的函数在完成工作前就会返回，而且在应用中触发一些将要进行的动作前，一般会在后台进行一些工作。这与一般的同步函数相反，同步函数在返回前会完成所有应该完成的事情。异步接口有很多种风格：

- Callback argument
- Return a placeholder (Future, Promise, Defered)
- Deliver to a queue
- callback registry (一个例子是 POSIX signals)

无论使用何种类型的接口，与同步函数相比，异步函数从定义上就与其调用方（callers）的交互方式不同，因此没有简单的方法可以让一个同步的函数以对其调用方透明的方式实现异步化。


### 几个例子

