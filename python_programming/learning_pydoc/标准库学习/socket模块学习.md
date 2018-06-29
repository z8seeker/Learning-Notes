# socket 模块学习

## socket families


## module contents


### exceptions


### constants


### functions


#### creating sockets


#### other functions

Looking up Hosts on the Network
- socket.gethostname(), 返回 python 解释器所在系统，在当前网络中的主机名
- socket.gethostbyname(hostname), 参数为主机名，返回 IPv4 地址的字符串表示。不支持 IPv6 地址解析
- socket.gethostbyname_ex(hostname), 参数为主机名，返回一个元组 `(hostname, aliaslist, ipaddrlist)` 。不支持 IPv6 地址解析
- socket.getfqdn([name]),  参数为部分主机名，参数为空时默认为 local host，返回 full qualified domain name
- socket.gethostbyaddr(ip_address), 参数为 IPv4/IPv6 地址， “反向” 查找主机名，返回一个元组 `(hostname, aliaslist, ipaddrlist)`




Finding Service Information

每个 socket address 除了 IP 地址以外，还包括一个整数的端口号。同一台主机上可以运行很多应用，这些应用都监听同一个 IP 地址，但一次只有一个 socket 可以使用该地址中的特定端口。

结合 IP 地址， 协议和端口号可以唯一标识出一个通信管道（communication channel），确保通过 socket 发送的信息正确的到达目的地。

- `socket.getservbyname(servicename[, protocolname])`，查找有标准化名字的网络服务的端口号。
- `socket.getservbyport(port[, protocolname])`, 参数为端口号，整型，反向查找网络服务名
- `socket.getprotobyname(protocolname)`, 参数为传输协议名，返回一个整型数，可以作为 `socket(...)` 函数的第三个参数


Looking Up Server Addresses

- socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0), 返回 a list of 5-tuples, 元组的结构： `(family type, proto, canonname, sockaddr)`, 利用返回的元组信息就可以与目标主机建立连接。



```python
import socket


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

for response in socket.getaddrinfo('www.python.org', 'http'):

    # Unpack the response tuple
    family, socktype, proto, canonname, sockaddr = response

    print('Family        :', families[family])
    print('Type          :', types[socktype])
    print('Protocol      :', protocols[proto])
    print('Canonical name:', canonname)
    print('Socket address:', sockaddr)
    print()
```
调用 `socket.getaddrinfo(...)` 函数时，可以指定参数值过滤结果列表， 其中 host 和 port 参数是必须的。可选参数是 family, socktype, proto, and flags，它们的值可以是 0 或是由 socket 定义的常量值。




IP Address Representations

### socket objects


socket 对象常用的方法：
- server socket methods
    - s.bind()，对 socket进行地址绑定，(host, port) 
    - s.listen()，建立并启动 TCP 监听
    - s.accept()，被动地接收 TCP 客户端连接，在连接到达前一直处于等待中（阻塞）
- client socket methods
    - s.connect()，与 TCP server 建立连接
    - s.connect_ex(),  发生错误时返回错误码，而不是抛出异常
- general socket methods
    TCP
    - s.recv()
    - s.send()
    - s.sendall()
    UDP
    - s.recvfrom()
    - s.sendto()
    - 
    - s.getpeername(), 连接到的 TCP socket 的远程地址
    - s.getsockname()，当前 socket 的地址
    - s.getsockopt(), 返回给定 socket 选项的值
    - s.setsockopt(), 设定 socket 选项的值
    - s.close()，关闭 socket
- blocking-oriented socket methods
    - s.setblocking()，设置 socket 模式为阻塞或非阻塞
    - s.settimeout()
    - s.gettimeout()
- file-oriented socket methods
    - s.fileno()，socket 的文件描述符
    - s.makefile(), 创建与 socket 相关联的 文件对象

### notes on socket timeouts


### example

