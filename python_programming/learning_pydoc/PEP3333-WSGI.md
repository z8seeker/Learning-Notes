# Python web server gateway interface

## 什么是 WSGI

在 `web 服务器` 与 `python 应用或 python 框架` 之间的标准接口，以便让使用 python 编写的 web 应用可以在多种 web 服务器之间进行移植（可以自由的选择使用 web 服务器）


## 提出 WSGI 的原因

在 WSGI 出现以前，python 开发者选择何种 web 框架将影响对可用 web 服务器的选择，反之亦然。

作为对比的是， Java 虽然有众多的框架，当因为有 `servlet` API，任何使用 java 编写的应用和框架都可以运行在支持 servlet API 的 web 服务器里。

WSGI 为 web 服务器和 python 应用之间提供了一个简单，通用的接口。除了实现简单，WSGI 也可以轻松的创建：

- request preprocessors, 
- response postprocessors, 
- and other WSGI-based "middleware" components
  - look like an application to their containing server, 
  -  while acting as a server for their contained applications

提出 WSGI 的短期目标是：Enable the use of any framework with any server

## WSGI 规范概览

WSGI 规范有两边：

- 服务器或网关端
- 应用或框架端

服务器端调用一个由 python app 提供的可调用对象（callable object），至于如何给服务器端提供这个对象，由服务器或网关来决定。

 It is assumed that some servers or gateways will require an application's deployer to write a short script to create an instance of the server or gateway, and supply it with the application object. 
 
 Other servers and gateways may use configuration files or other mechanisms to specify where an application object should be imported from, or otherwise obtained.

 除了纯粹的服务器/网关，应用/框架之外，还可以创建中间件组件（需要同时实现两端的规范）。中间件可以提供如下的功能：

 - extended APIs, 
 - content transformation, 
 - navigation, 
 - and other useful functions.

 
 词语约定：

 一个 callable 可以是：

 - a function
 - a method
 - a class
 - an instance with a `__call__` method

在 WSGI 规范中可调用对象仅仅只是用来进行调用的，而不应该用来进行反射（自省）

### 关于字符串类型

python 的字符串是最方便处理文本的数据结构，而 python 中的字符串是 Unicode 对象而不是 bytes 对象，而 HTTP 协议处理的则是字节流。 WSGI 为此定义了两种类型的“字符串”：

- "Native" strings，使用 `str` 类型实现，用于处理 request/response 头和 metadata
- "Bytestrings"，在 python3 中使用 `bytes` 类型实现，python2 中使用 `str` 类型实现，用于处理请求和响应的 body 部分

即使是 python 的 `str` 类型，实际上幕后也是 unicode （under the hood），native strings 的内容仍然必须使用 `Latin-1` 编码被转换为 bytes 对象。

### 应用或框架端

application 对象就是一个接收两个参数的可调用对象而已。application 对象必须可以被多次调用，因为所有的 servers/gateways 都会发出调用请求。应用对象返回的是响应体(response body)，必须是一个可迭代的字节字符串（Bytestrings）（an iterable of byte strings）。

下面是两个 application 对象的例子，一个 application 对象是函数， 而另一个则是一个类：

```python
HELLO_WORLD = b"Hello world!\n"


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


class AppClass:
    """
    'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(environ, start_response):
        self.environ = environ
        self.start = startt_response
    
    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
```

`start_response` 也是一个可调用对象，接受两个位置参数：`status`, `response_headers`


### 服务器或网关端

服务器或网关端每接到一次 HTTP 客户端的请求就会调用 application callable 对象

```python
import os
import sys

from app import simple_app


def run_with_cgi(application):
    environ = dict(os.environ.items())
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            sys.stdout.write('Status: %s\r\n' % status)
            for header in response_headers:
                sys.stdout.write('%s: %s\r\n' % header)
            sys.stdout.write('\r\n')

        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()

if __name__ == '__main__':
    run_with_cgi(simple_app)
```

### 中间件：游走于两端之间的组件

一个对象在面向应用时可以扮演服务器的角色，在面向服务器时由可以扮演应用的角色，这就是 "middleware"。中间件自身也是一个 WSGI 应用，通过委托其他 WSGI 应用来处理用户求，中间件可以实现以下的功能：

- 将一个请求路由到不同的 application 对象去处理。方法是基于 target URL，重写 environ 变量
- 允许多个应用或框架在同一个进程里 run side-by-side
- 实现负载均衡和远程处理。方法是通过网络转发请求和响应
- 执行内容的后处理，比如应用 XSL 样式

中间件总体而言应该对服务器和应用是透明的，而且不需要特别的支持。因此一个中间件可以包裹另一个中间件，形成一个 "middleware stack"。

## WSGI 规范的细节

应用对象必须接受两个参数：environ 和 start_response。而服务器或网关必须使用位置参数（不能是关键字参数）调用应用对象：

```
result = application(environ, start_response)
```

`environ` 参数是一个字段对象，包含了 CGI-风格的环境变量信息，这个对象必须是 python 的内置字典对象（不能是子类，UserDict 或其他的字典模拟对象），应用对象应该可以对这个字典对象作出任意修改。enrion 参数必须包含 WSGI-required 的参数，也可以包含服务器特定的扩展参数。

`start_response` 参数是一个必须接收两个位置参数和一个可选参数的可调用对象，而当应用调用 start_response 时必须使用位置参数：

```
start_response(status, response_headers, exc_info=None)
```

`status` 参数是一个表示 HTTP 状态码的字符串，比如 `999 Message here`，`response_headers` 是由一系列 (header_name, header_value) 元组组成的列表，用来描述 HTTP 响应头。

`start_response` 可调用对象，必须返回一个可调用对象 `write(body_data)`，这个可调用对象接受一个位置参数（Bytestrings）作为 HTTP 响应的 body。

当应用对象被服务器调用时，必须返回一个可迭代对象，产出 0 个或多个 Bytestrings，这可以通过多种方式实现：

- 返回一个由 Bytesrings 组成的列表
- 应用对象是一个产出 Bytestrings 的生成器函数
- 应用对象是一个实例为可迭代对象的类

服务器或网关必须将产出的 Bytestrings 传递给客户端（in an unbuffered fashion），在完成应用对象返回的所有 Bytestrings 后， 服务器或网关才可以继续处理其他请求。

服务器或网关应该将产出的 Bytestrings 作为二进制字节序列进行处理。 应用对象负责保证字节字符串的格式是适合于客户端的。

如果 `len(iterable)` 可以调用成功，服务器必须可以认为这个结果是准确的。如果由应用对象返回的 iterable 有 `close()` 方法，服务器或网关在完成当前这个请求后必须调用这个方法，无论这个请求是否被正常处理。

应用对象如果返回一个生成器或其他定制的迭代器时，不应该认为整个迭代器都会被全部迭代一遍，因为服务器有可能提前关闭。

应用对象必须先调用 `start_response`，然后 iterable 再产出 Bytestrings （响应体），这样服务器才能在发送 HTTP body 内容前先发送 HTTP 响应头。然而这个调用（指调用 `start_response`）也可以在 iterable 的第一次迭代时执行。

服务器或网关一定不能直接使用由应用对象返回的 iterable 的其他属性，除非这个 iterable 对服务器或网关而言是特定类型的对象。

### environ 变量

environ 字典必须要包含有 CGI 规范定义的环境变量，下面的变量必须要出现，除非它们的值是空的字符串：

- `REQUEST_METHOD`, HTTP 请求方法，不能为空
- `SCRIPT_NAME`, the initial portion of the request URL's "path"
- `PATH_INFO`, the remainder of the request URL's "path"
- `QUERY_STRING`, the portion of the request URL that follows the "?"
- `CONTENT-TYPE`, HTTP 请求中 Content-Type 字段的内容
- `CONTENT-LENGTH`, HTTP 请求中 Content-Length 字段的内容
- `SERVER_NAME, SERVER_PORT`, used to complete the URL, can never be empty strings
- `SERVER_PROTOCOL`, 客户端发送请求时使用的协议版本 "HTTP/1.1"
- `HTTP_Variables`

服务器或网关应该提供尽可能多的 CGI 环境变量信息。CGI-defined 变量必须是 native strings。

除了 CGI-defined 的变量，environ 字典里还可以包含任意数量的操作系统的环境变量，而且也必须包含下面的 WSGI-defined 变量：

- `wsgi.version`, the tuple (1, 0)
- `wsgi.url_scheme`, a string, "http" or "https"
- `wsgi_input`, an input stream from which the HTTP request body bytes can be read
- `wsgi.errors`, an output stream to which error output can be written
- `wsgi.multithread`,  true or false
- `wsgi.multiprocess`, true or false
- `wsgi.run_once`, this will only be true for a gateway based on CGI

最后， environ 字典还可以包含 server-defined 变量，这些变量应该以 小写字母，数字，点，下划线表示，比如 `mod_python` 可以这样定义一个变量 `mod_python.some_variable`

### `start_response()` 可调用对象

### 缓冲与流

### unicode 问题

### 错误处理
