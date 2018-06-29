# socketserver 模块

## 概述

这是一个用于创建 network servers 的框架。模块里定义了用于处理 _同步网络请求_ （TCP, UDP, Unix streams, Unix datagrams）的类，同时也提供了 mix-in 类用于将服务器转换成多线程或多进程服务器。

对于每种类型的服务器，处理网络请求的职责被划分为以下两部分：

1. 用于处理通信相关问题，包括：监听端口，接收连接等。这些功能通过 server class 实现
2. 用于处理“应用协议”相关问题，包括：解析请求数据，处理请求，发送响应。这些功能由用户自定义的 request handler class 实现。 


这种职责划分方法，可以让很多应用：

- 只需少量修改即可直接使用 server class，
- 然后再提供一个定制的 request handler class 


### 服务器类型

socketserver 模块里有五个不同的服务器类：

1. BaseServer, 定义了 API（接口），不能直接实例化使用
2. TCPServer, 使用 TCP/IP sockets 进行通信
3. UDPServer, 使用 datagram sockets 进行通信
4. UnixStreamServer, 使用 Unix streams 通信，只能用于 UNIX 平台
5. UnixDatagramServer, 使用 Unix datagrams 通信， 只能用于 UNIX 平台

它们之间的关系如下所示：

```
    +------------+
    | BaseServer |
    +------------+
          |
          v
    +-----------+        +------------------+
    | TCPServer |------->| UnixStreamServer |
    +-----------+        +------------------+
          |
          v
    +-----------+        +--------------------+
    | UDPServer |------->| UnixDatagramServer |
    +-----------+        +--------------------+

```

不管这些服务器类使用哪一种协议，它们都有相同的：

- 外部的方法（external methods）
- 属性（attributes）

### 创建服务器

我们创建自己的服务器时，通常只需要使用 socketserver 模块里提供的四个服务器类（ TCPServer, UDPServer, UnixStreamServer, UnixDatagramServer）中的某一个。实例化服务器对象时，需要传递两个参数：

1. address，服务器在这个地址监听请求。地址的格式由服务器的类型和 socket 的地址家族决定
2. request handler class，这是继承自 `BaseRequestHandler` 类的请求处理类（并重写了用于处理请求的 `handle()` 方法），需注意 _不是实例_

如果有其他特殊情况，我们也可以定制自己的服务器类（继承自 BaseServer），重写 BaseServer 类的某些方法，比如：

- `verify_request(request, client_address)`, 通过定制这个方法可以拒绝某个 IP 段的请求，或当服务器过载时拒绝请求，等等
- `process_request(request, client_address)`, 通过定制这个方法可以在一个独立的线程或进程里处理请求，等等
- `finish_request(request, client_address)`, 使用请求处理类创建一个实例，然后调用实例的 `handle()` 方法处理请求

一旦实例化服务器对象以后，推荐在 `with` 语句里使用服务器对象的以下两种方法处理请求：

1. `serve_forever()`
2. `hanlde_request()`

`serve_forever()` 方法是在一个无限循环里调用 `hanlde_request()` 方法。如果我们的应用需要把服务器集成到另一个 event loop 里或需要使用 `select()` 同时监控多个不同服务器的 sockets 时，则可以直接调用  `hanlde_request()`  方法


### Request Handlers (请求处理类)

Request Handlers 接收从远端传来的数据，进行处理并生成响应返回。从网络层次模型的角度来说，Request Handlers 负责 socket 层上方，也就是应用层协议的实现（HTTP, XML-RPC, AMQP, 等等）。

在具体实现时，可以重写 Request Handlers 的以下某些方法，比如：

- `setup()`, 用于准备 request handler，
- `handle()`, 用于处理请求，负责解析请求数据，处理数据，并发送响应
- `finish()`, 清理在 `setup()` 阶段创建的对象

通常很多应用的请求处理类只需要实现一个 `handle()` 方法就可以了。


## 服务器类与 MixIn 机制


### class BaseServer 类

模块中的其他服务器类都直接或间接继承 BaseServer, BaseServer 类定义了处理请求的 API。BaseServer 的构造函数 `__init__` 需要传入两个参数：

- server_address
- RequestHandlerClass


#### 类变量

- `allow_reuse_address`, 用于确定是否允许服务器重用地址，默认值为 False （不允许）
- `request_queue_size`, 用于确定请求队列的大小，当处理一个耗时较长的请求时，新到达的请求将被放到这个队列中，当队列已满后，从客户端继续发出的请求将会产生 `Connection denied` 的错误。默认值为 5
- `address_family`, 服务器使用 socket 的地址家族
- `socket_type`, 服务器使用的 socket 种类
- `timeout`, 超时设置，单位为秒，如果不需要设置超时的话，可设为 `None`。如果设置了超时，且在设置时间内 `handle_request()` 没有收到新请求的话，将调用 `handle_timeout()` 方法


#### 实例变量

- RequestHandlerClass, 使用者提供的请求处理类，对于每一个到来的请求通过创建一个新实例进行处理
- socket, 用于监听请求的 socket 对象


#### 请求处理

##### handle_request() 方法

`handle_request()` 是顶层调用，它在内部调用:

- `selector.register(selectors.EVENT_READ)`
- `selector.select(timeout)`
- `_handle_request_noblock()`, 因为通过 `selector.select()` 已经返回了可读的 socket，所以是非阻塞的。其在内部调用
    - `get_request()`, 获取与客户端进行通信的一个新 socket 对象和客户端地址
    - `verify_request(request, client_address)`，判断是否需要处理请求，如果需要处理处理：
        - `process_request(request, client_address)`, 其在内部调用：
            - `finish_request(request, client_address)`, 这是实际处理请求的方法，在内部通过 _实例化请求处理类_ 完成对请求的处理
            - `shutdown_request(request)`, 停止并关闭特定的一个请求，其在内部调用：
                - `close_request(request)`, 清理具体的某个请求，内容为空需要子类进行覆盖
        - `handle_error(request, client_address)`, 默认打印 traceback 信息, 然后继续监听请求
    - `shutdown_request(request)`, 当判断不需要处理请求时，停止并关闭特定的这个请求
- `handle_timeout()`, 在 timeout 时间内没有新请求时调用。内容为空，需要子类进行覆盖

`get_request()` 方法用于获取客户请求和客户地址，对于不同种类的 sockets 而言，实现方法各异。这个方法需要返回：

1. 客户端请求, request
2. 客户端地址, request_address

`verify_request()` 方法用于验证请求，以确定是否需要处理该请求。该方法返回：

- `True`, 则继续处理请求
- `False`, 则丢弃请求，不再做处理

`process_request()` 方法用于处理请求：

1. 通过调用 `finish_request(request, client_address)` 方法使用由构造函数传入的请求处理类 `RequestHandlerClass` 处理请求；
2. 通过调用 `shutdown_request(request)` 方法使用 `close_request(request)` 方法清理并关闭请求


请求处理方法覆盖情况：

- `process_request()` 方法被 `ForkingMixIn` 类和 `ThreadingMixIn` 类所覆盖，用于并发处理请求。
- `handle_timeout()` 方法被 `ForkingMixIn` 类覆盖


#### 服务启动

- `server_activate()`， 在构造函数里进行调用，启动服务器，可以被子类覆盖
- `serve_forever(poll_interval=0.5)`, 处理请求，直到遇到显式的调用 `shutdown()` 请求时才会终止。每隔 `poll_interval` 时间轮询是否遇到  `shutdown`。此外，还在内部调用：
    - `service_actions()`, 可以用于子类或 mixin 类中，完成特定的操作。比如：在 `ForkingMixIn` 类中这个方法用于清理僵尸子进程。


#### 服务关闭

- `shutdown()`, 停止 `serve_forever` 循环，这个方法将阻塞，直到循环完成为止。使用这个方法时，必须确保 `serve_forever` 在另一个线程运行，否则将发生死锁。
- `server_close()`, 清理服务器，内容为空需要子类进行覆盖

BaseServer 类实现了上下文管理器协议，在 `__exit__(*args)` 方法里调用了 `server_close()` 方法。


#### 小结

可以被子类覆盖的方法如下：

- `server_bind()`, 在服务器的构造函数里将 socket 绑定到想要监听的地址上
- `server_activate()`
- `get_request()`
- `handle_timeout()`
- `verify_request(request, client_address)`
- `process_request(request, client_address)`
- `finish_request(request, client_adderss)`
- `shutdown_request(request)`
- `close_request(request)`
- `service_actions()`
- `server_close()`
- `handle_error(request, client_address)`, 如果 `RequestHandlerClass` 实例的 `handle()` 方法抛出异常时，将调用此方法

对于服务器对象的外部用户而言（调用服务器对象的用户），上面这些方法对其是透明的（意思是：不可见，不用直接调用或没有用的）。换句话说，服务器类的外部用户只需调用以下方法（external methods）：

- `__init__(server_address, RequestHandlerClass)`
- `serve_forever(poll_interval=0.5)`
- `handle_request()`
- `shutdown()`
- `fileno()`, 用于 selector 接口

即可完成自己的目标任务。




### ThreadingMixIn

使用继承 ThreadingMixIn 的服务器类在使用多线程处理请求时，当发生意料外的中断时需要显式的声明线程应进行的操作。ThreadingMixIn 类定义了 `daemon_threads` 属性，指示服务器对象是否需要等待线程终止，这个值默认为 `False`，意味着只有当 `ThreadingMixIn` 创建的所有线程都退出以后，python 才会退出。

请求处理过程：

- `process_request(request, client_address)`， 在一个新线程里处理请求
    - `process_request_thread(request, client_address)` , 请求处理逻辑与异常处理
        - `finish_request(request, client_address)`,  与 BaseServer 中的一致
        - `handle_error(request, client_address)`,  与 BaseServer 中的一致
        - `shutdown_request(request)`, 与 TCPServer 或 UDPServer 中的一致


