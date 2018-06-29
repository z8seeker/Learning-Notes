# Socket Programming HOWTO

### 1. sockets 概述

INET (i.e. IPv4) sockets --> STREAM (i.e. TCP) sockets --> non-blocking sockets --> blocking sockets

在不同的上下文中， socket 指代着不同的东西，本文对 socket 做以下区分：

- a "client" socket: an endpoint of a conversation
- a "server" socket: like a switchboard operator
- the client app uses "client" sockets exclusively
- the web server uses both "server" sockets and "client" sockets


### 2. 历史

在各种形式的 IPC （进程间通信）中， sockets 是最流行的。而对于跨平台通信的 IPC， sockets 则是唯一的选择。Sockets 由 Berkeley 发明，作为 BSD Unix 的一部分。Sockets 可以很轻松的实现任意机器间的对话，因此很快在整个 Internet 流行开来。

### 3. 创建一个 Socket

创建一个 client socket:

```python
# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(('www.python.org', 80))
```

当 connect 完成以后，socket s 可以发送请求 (request)，然后读取回复 (reply)，最后被销毁。client socket 一般只进行一次交互。而 web
server 的情况要相对复杂一些：

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
- 数值较低的端口号一般是为常见的服务而保留的（HTTP, SNMP etc)
- `listen` 告诉 socket 库，最多在队列里保持 5 条连接请求（将拒绝超过5条之外的请求），如果代码组织得当的话，5 条就足够用了

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


### 4. IPC
若要在一台机器上的两个进程间实现快速的 IPC，应该使用 pipes 或者 shared memory。 

标准库里的 multiprocessing 模块集成了用于进行跨平台 IPC 的 API


### 5. 使用 Socket

需要指出的一点是， 浏览器的 "client" socket 与 web server 的 "client" socket 是完全一样的东西。二者之间是 "peer to peer" 通信，也就是说，我们要规定二者通信的规则 （因为sockets 对此不做任何规定）。通常的做法是，进行连接的 socket 通过发送请求发起会话。

可以使用两组动词实现 sockets 之间的通信：
- `send` and `recv`
- 或者将 client socket 转为 file-like 对象，然后使用 `read` and `wirte`
    - 需要对 socket 执行 `flush` 操作，否则在进行 read 时将一直处于 wait 状态
    - 这是因为 request 数据 仍然在输出缓冲区中


`send` 和 `recv` 对网络缓冲区 (network buffers) 的操作：

- send 和 recv 并不是对（not necessarily）我们交给它们的 __所有字节__ 进行处理，而是主要处理 network buffers。 

- In general, they return when the associated network buffers have been filled (send) or emptied (recv). 

- 然后它们告诉我们它们处理了多少字节，我们需要主动地反复调用它们，直到我们的消息被全部处理完

- 当 `recv` 返回 0 字节时，意味着连接的另一侧已经关闭连接（或正在关闭），此后将不会在这个连接上收到任何数据，但有可能成功发送数据

像 HTTP 这样的协议，使用一个 socket 仅仅进行一次数据传输： client 发送一个请求，然后读取响应，之后这个 socket 就被丢弃了。这也意味着 client 可以侦测到响应的结束（by receiving 0 bytes）


如果我们想重用（reuse） socket，我们需要意识到在 socket 中并不存在 EOT （end of transmission）传输结束符。如果一个 socket `send` 或 `recv` 返回 0 bytes 时， 这个连接就不可用了（broken）。如果连接还没被 broken，我们可能一直处于等待 `recv` 的状态，这是因为 socket 不会告诉我们目前没有需要 read 的数据了 （for now）。当我们考虑到以上这些时，我们会发现关于 socket 的一个基本事实，消息必须：
- 或者是 fixed length （yuck）
- 或者是 delimited （使用分隔符，shrug）
- 或者明确表明长度 （much better）
- 或者以关闭连接作为结束 （end）

如果我们不想关闭连接，最简单的方法是使用固定长度的消息（a fixed length message）:

```python
class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - byte_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

```
增强上面程序的几个方法：
1. 使消息的第一个字符表示信息类型，然后使用这个类型信息确定消息长度
2. 如果使用 delimited 的方法，我们可能接收到任意长度的数据（4096,8192 is frequently a good match）
3. 为消息加上一个长度前缀（say, as 5 numeric characters），但是在 high network loads 时，我们可能不会在一次 `recv` 时就全部收到这 5 个字符。除非我们进行两次 `recv` 循环：第一次确定消息的长度；第二次获得消息的数据。


### 6. Binary Data

对于二进制数据的最大问题是不同机器间可能有不同的表示格式


### Disconnecting

严格意义上讲，我们应该在 `close` socket 前先进行 `shutdown` 操作。然而绝大部分 socket 库只需使用一个 `close` 就和 `shutdown(); close()` 一样，因此一般不需显示的使用 `shutdown`

一个显示使用 shutdown 的场景是在进行 HTTP-like 的数据交换时，client 发送一个请求，然后执行 `shutdown(1)` 。 这将告诉服务器“client 已经完成发送， 但仍然可以接收数据”。服务器可以探测到 “EOF”（接收到 0字节），可以确定收到了完整的请求。当服务器发送响应后，实际上，client 仍然处于接收状态（still receiving）

please close your sockets when you're done.


### When sockets die

使用阻塞 sockets 时发生的最坏事情可能就是另一侧的 socket comes down hard （without doing a close），这时我们的 socket 可能处于挂起状态（hang），这是因为 TCP 可能会等很长很长时间才会放弃这个连接。


### Non-blocking sockets

在 python 里 使用 `socket.setblocking(0)` 可以将 socket 设置为 non-blocking 式的。与阻塞式的主要机制上的区别是：
- `send`, `recv`, `connect`, `accept` 可以在没有做任何工作时就返回
- 使用 non-blocking sockets 的正确方式是使用 select


```python

ready_to_read, ready_to_write, in_error =\
    select.select(
        potential_readers,
        potential_writers,
        potential_errs,
        timeout)

```