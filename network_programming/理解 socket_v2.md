# 理解 socket

本文讲述什么是 socket，sokcket 的种类以及使用 python 进行 socket 编程的方法，具体包括以下内容：

- [什么是 socket](#什么是-socket)
- [socket 的种类](#socket-的种类)
  - [unix domain sockets](#unix-domain-sockets)
  - [network sockets](#network-sockets)
  - [connection-oriented versus connectionless](#connection-oriented-versus-connectionless)
    - [connection-oriented](#connection-oriented)
    - [connectionless](#connectionless)
- [使用 Python 进行网络编程](#使用-python-进行网络编程)
  - [python 支持的 socket 种类](#python-支持的-socket-种类)
  - [TCP server and client](#tcp-server-and-client)
    - [创建 TCP 服务器](#创建-tcp-服务器)
    - [创建 TCP 客户端](#创建-tcp-客户端)
    - [更好的使用 socket 进行 TCP 通信](#更好的使用-socket-进行-tcp-通信)
  - [UDP server and client](#udp-server-and-client)
    - [创建 UDP 服务器](#创建-udp-服务器)
    - [创建 UDP 客户端](#创建-udp-客户端)
  - [其他相关的模块](#其他相关的模块)

## 什么是 socket

sockets 本质上是用于进程间通信的 API，最初由 Berkeley 发明，作为 BSD Unix 的一部分, 也叫 BSD sockets。

## socket 的种类

有两种类型的 sockets：

1. unix domain sockets, 也叫 IPC socket
2. network sockets, 也叫 Internet socket

在讨论这两种类型的 socket 之前，需要先介绍一下 _文件描述符_ 的概念。

一个文件描述符是一个正整数， 当一个进程打开一个存在的文件，创建一个新文件或创建一个新的套接字的时候，内核返回一个正整数给进程，这个正整数就是文件描述符。 你可能听说过，在 UNIX 中一切皆文件。 内核通过文件描述符来索引一个进程打开的文件。 当你需要读或写一个文件时，你需要用文件描述符来标记它。

默认情况下，UNIX shell 给一个进程的标准输出分配的文件描述符是 0， 标准输入的文件描述符是 1，标准错误的文件描述符是 2。

```python
import sys
import os

sys.stdin.fileno()  # 0

sys.stdout.fileno()  # 1

sys.stderr.fileno()  # 2

res = os.write(sys.stdout.fileno(), b'hello\n')  # 'hello'

````
描述符的概念就介绍到这里，下面继续讨论 socket。

### unix domain sockets

unix domain sockets 是一个数据通信端点，用于在同一个系统中的不同进程间交换数据。unix domain sockets 的通信不依赖于底层的网络协议，所有的通信全部在操作系统内核中完成。unix domain sockets 使用文件系统作为自己的地址名称空间（address name space）， 进程引用的 unix domain sockets, 是作为文件系统的索引结点 (inodes)，因此两个进程可以通过打开的同一个 socket 进行通信。

unix domain sockets 的地址家族名字是 `AF_UNIX`, 意思是 "address family: UNIX"。

总结：

- unix domain sockets (UDS), 在 POSIX 兼容的系统中可用
- 在进程间传递数据不用通过 network stack，比 `AF_INET` 更高效
- 与其他 IPC 机制（named pipes, shared memory）相比，优点是编程接口与 IP networking 一致

### network sockets

network socket 是计算机网络中的一个节点用于发送或接收数据的一个内部端点。具体的说, 一个 network socket 是对协议栈中一个端点的表示（用于获取通信协议，目的地，状态等信息的入口），是一种系统资源。

进程通过使用 `socket descriptor`（通常在内部表示为一个整数） 引用 socket。进程首先请求协议栈创建一个 socket，然后协议栈向进程返回一个 `socket descriptor`。当进程需要使用 socket 发送或接收数据时，就把这个 `socket descriptor` 传递给协议栈。

network sockets have two primary properties controlling the way they send data:

- the address family controls the OSI network layer protocol used
- the socket type controls the transport layer protocol

networked sockets 的常用地址家族名字是:

- `AF_INET`, 意思是 "address family: Internet", 用于 IPv4 addressing
- `AF_INET6`, 用于 IPv6 addressing

除此之外，还有其他的地址家族，但应用最广泛的是：`AF_INET`。

### connection-oriented versus connectionless

不管使用哪一种地址家族的 socket，都有两种风格的 socket connections：

1. connection-oriented, or stream-oriented
2. connectionless, or message-oriented

#### connection-oriented

只有当建立了连接以后，sockets 间才能进行通信。这种类型的通信也叫做：

- virtual circuit
- stream socket

connection-oriented 通信提供 _有序的、可靠的和不重复的数据传输_。实现这种连接类型所用的协议是 `Transmission Control Protocol` (TCP) 。为了创建一个 TCP socket，必须使用 `SOCK_STREAM` 作为 socket 的类型。因为这些 TCP socket 使用 `Internet Protocol` (IP) 找到网络中的目标主机， 因此整个系统一般被叫做: `TCP/IP`。

对于需要保持信息可靠和有序的应用协议，可使用 TCP 协议进行通信，如 HTTP 协议。

#### connectionless

在通信开始前不需要建立连接, 这种类型的通信也叫做： datagram socket。Connectionless 通信过程中, 传送数据的有序性，可靠性和不重复性没有保证，通常一次传送整个完整消息。相比 connection-oriented socket， datagram 有更好的性能。

实现这种连接类型所用的协议一般是 `User Datagram Protocol` (UDP)。为了创建一个 UDP socket 我们必须使用 `SOCK_DGRAM` 作为 socket 的类型。因为这些 UDP socket 使用 `Internet Protocol` (IP) 找到网络中的目标主机， 因此整个系统一般被叫做: `UDP/IP`。

对于信息有序性不敏感（因为消息是 self-contained, 而且通常是短消息）或需要进行多路广播（multi-casting）的应用协议而言，可以使用 UDP 进行通信，如 DNS 协议。

## 使用 Python 进行网络编程

### python 支持的 socket 种类

python 支持上面说的几种地址家族：

- AF_UNIX
- AF_INET*

在 Python 2.5 中引入了对一类特殊 Linux socket 的支持：`AF_NETLINK` (connectionless)。这种 socket 使用标准的 BSD socket 接口 允许用户代码与内核级代码进行 IPC。

此外， Python 还支持其他地址家族的 socket，具体可以查看 socket 模块的文档。

网络编程是指使用 network socket 编写应用程序, 因此以下将只针对 network socket 进行讨论。


标准库中的 socket 模块中有一个 `socket()` 函数，用于创建 socket 对象。socket 对象有一组方法，可以实现基于 socket 的网络通信。

使用 `socket.socket()` 函数创建 socket 对象的语法：

`socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)`

对函数中的参数的说明如下：

family:

- AF_UNIX
- AF_INET*
- AF_CAN
- AF_RDS

type:

- SOCK_STREAM
- SOCK_DGRAM
- SOCK_RAW

proto: 协议编号通常设为 0

fileno: 如果指定了 fileno 的值，则函数的其他参数都将被忽略，将返回这个文件描述符指向的 socket

### TCP server and client

在接下来的讨论中，在不同的上下文中 socket 指代着不同的东西，需要对 socket 做以下区分：

- a "client" socket: an endpoint of a conversation
- a "server" socket: like a switchboard operator (总机接线员)
- the client app uses "client" sockets exclusively
- the web server uses both "server" sockets and "client" sockets

#### 创建 TCP 服务器

创建 TCP 服务器的常用套路，使用伪代码说明如下：

```code

ss = socket()  # 创建服务器 socket
ss = bind()  # 绑定地址
ss.listen()  # 监听连接
inf_loop:  # 服务器无限循环
    cs = ss.accept()  # 接收客户端连接
    comm_loop:  # 用于通信的循环
        cs.recv/cs.send()  # 对话
    cs.close()  # 关闭 cilent socket
ss.close()  # 关闭 服务器 socket
```

默认情况下， `accept()` 方法是阻塞的：

- 程序执行到这里将处于挂起状态
- 直到有连接请求过来，才会继续向下运行

一旦接收连接后， `accept()` 方法将返回一个 client socket 用于接下来的信息通信。

接下来使用 python 程序进行详细讨论：

```python
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 80))
# become a server socket
serversocket.listen(5)
```

注意事项：

- 使用 `socket.gethostname()`, the socket would be visiable to the outside world
- 若使用 ```s.bind(('localhost`, 80))``` 或 ```s.bind(('127.0.0.1', 80))```, only visiable within the same machine.
- 数值较低的端口号 (< 1023) 一般是为常见的服务而保留的（HTTP, SNMP etc)
- `listen` 告诉 socket 库，最多在队列里保持 5 条连接请求（将拒绝超过5条之外的请求），如果代码组织得当的话，5 条就足够用了。

接下来，进入 web server 主循环：

```python
while True:
    # accept connections from outside
    (cilentsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()
```

主循环里实际可以有 3 种工作方式：

1. dispatching a thread to handle cilentsocket
2. create a new process to handle clientsocket
3. restrcuture this app to use non-blocking sockets, multiplex between our "server" socket and any active clientsocket using `select`

 一个 "server" socket 全部的工作都在主循环里完成：
 - 它不发送任何数据
 - 它不接收任何数据
 - 它仅仅只是产生 "client" sockets
 
当其他 "client" socket 执行 `connect()` 连接到 "server" socket 绑定的 (host, port) 时， "server" socket 将对此做出响应并创建一个 clientsocket。clientsocket 一旦创建完毕，"server" socket 将回头 (go back) 继续监听其他的连接请求。这两个 "clients" (socket) 使用动态分配的端口 (port) 自由的进行通信，通信完毕后该端口将被回收。

#### 创建 TCP 客户端

创建 tcp 客户端的常用套路，使用伪代码表示如下：

```code
cs = socket()  # 创建客户端 socket
cs.connect()  # 尝试连接服务器
comm_loop:  # 通信循环
    cs.send()/cs.recv()  # 对话
cs.close()  # 关闭客户端 socket
```
客户端 socket 建立以后，通过使用 `connec()` 方法与服务器建立连接，然后可以与服务器通信。

接下来使用 python 程序进行详细讨论：

```python
# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(('www.python.org', 80))
```

当 connect 完成以后，socket s 可以发送请求 (request)，然后读取回复 (reply)，最后被销毁。client socket 一般只进行一次交互。

#### 更好的使用 socket 进行 TCP 通信

需要指出的一点是， 浏览器的 "client" socket 与 web server 的 "client" socket 是完全一样的东西。二者之间是 "peer to peer" 通信，也就是说，我们要规定二者通信的规则 （因为 sockets 对此不做任何规定）。通常的做法是，进行连接的 socket 通过发送请求发起会话。

可以使用两组动词实现 sockets 之间的通信：

- `send` and `recv`
- 或者将 client socket 转为 file-like 对象，然后使用 `read` 和 `wirte`
  - 需要对 socket 执行 `flush` 操作，否则在进行 read 时将一直处于 wait 状态，这是因为 request 数据仍然在输出缓冲区中


`send` 和 `recv` 对网络缓冲区 (network buffers) 的操作：

- send 和 recv 并不是对（not necessarily）我们交给它们的 __所有字节__ 进行处理，而是主要处理 network buffers。

- In general, they return when the associated network buffers have been filled (send) or emptied (recv).

- 然后它们告诉我们它们处理了多少字节，我们需要主动地反复调用它们，直到我们的消息被全部处理完

- 当 `recv` 返回 0 字节时，意味着连接的另一侧已经关闭连接（或正在关闭），此后将不会在这个连接上收到任何数据，但有可能成功发送数据

像 HTTP 1.0/1.1 这样的协议，使用一个 socket 仅仅进行一次数据传输： client 发送一个请求，然后读取响应，之后这个 socket 就被丢弃了。这也意味着 client 可以侦测到响应的结束（by receiving 0 bytes）


如果我们想重用 socket，我们需要意识到在 socket 中并不存在 EOT （end of transmission）传输结束符。如果一个 socket `send` 或 `recv` 返回 0 bytes 时， 这个连接就不可用了（broken）。如果连接还没被 broken，我们可能一直处于等待 `recv` 的状态，这是因为 socket 不会告诉我们目前没有需要读的数据了。当我们考虑到以上这些情况时，我们会发现关于 socket 的一个基本事实，消息必须：

- 或者是 fixed length （yuck）
- 或者是 delimited （使用分隔符，shrug）
- 或者明确表明长度 （much better）
- 或者以关闭连接作为结束 （end）

Disconnecting

严格意义上讲，我们应该在 `close` socket 前先进行 `shutdown` 操作。然而绝大部分 socket 库只需使用一个 `close` 就和 `shutdown(); close()` 一样，因此一般不需显示的使用 `shutdown`

一个显式使用 shutdown 的场景是在进行 HTTP-like 的数据交换时，client 发送一个请求，然后执行 `shutdown(1)` 。 这将告诉服务器“client 已经完成发送， 但仍然可以接收数据”。服务器可以探测到 “EOF”（接收到 0字节），可以确定收到了完整的请求。当服务器发送响应后，实际上，client 仍然处于接收状态（still receiving）

Please close your sockets when you're done.

When sockets die

使用阻塞 sockets 时发生的最坏事情可能就是另一侧的 socket comes down hard （without doing a close），这时我们这一侧的 socket 可能处于挂起状态（hang），这是因为 TCP 可能会等 _很长很长_ 时间才会丢弃这个连接。

Non-blocking sockets

在 python 里使用 `socket.setblocking(0)` 可以将 socket 设置为 non-blocking 式的。与阻塞式的主要机制上的区别是：

- `send`, `recv`, `connect`, `accept` 可以在没有做任何工作时就返回
- 使用 non-blocking sockets 的正确方式是使用 `select`

```python
ready_to_read, ready_to_write, in_error =\
    select.select(
        potential_readers,
        potential_writers,
        potential_errs,
        timeout)
```

### UDP server and client

#### 创建 UDP 服务器

创建 UDP 服务器的常用套路，使用伪代码表示如下：

```code
ss = socket()  # 创建服务器 socket
ss.bind()  # 绑定地址
inf_loop:  # 服务器无限循环
    cs = ss.recvfrom()/ss.sendto()  # 会话
ss.close() # 关闭服务器 socket
```

#### 创建 UDP 客户端

创建 UDP 客户端的常用套路，使用伪代码表示如下：

```code
cs = socket()
comm_loop:  # 通信循环
    cs.sendto()/cs.recvfrom()
cs.close()
```

### 其他相关的模块

- socketserver
- select，在一个单线程的网络服务器应用中管理多个 socket 连接
- selectors
- asyncore/asynchat
- asyncio
