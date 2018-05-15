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

下面是一个简单的同步函数：

```python
from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body
```

使用 callback argument 重写成异步函数后的样子：

```python
from tornado.httpclient import AsyncHTTPClient

def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)
    
    http_client.fetch(url, callback=handle_response)
```

使用 Future 而不是 callback 重写后的样子如下：

```python
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result())
    )
    return my_future
```

The raw `Future` 版本更加复杂，但却是 tornado 推荐的方案，这是因为使用 future 有两个优点：

- 异常处理与同步程序更加一致，`Future.result` 方法可以直接抛出异常
- `Future` 对象非常适合与协程一起使用（lend themselves well with coroutines）

使用协程重写上面的示例函数，可以发现与同步程序版本非常相似：

```python
from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
```

在 python2 里生成器不允许有返回值，为了从协程里返回一个值，tornado 可以抛出一个 Return 的特殊异常，协程会捕获这个异常并把它作为返回值处理。在 Python 3.3 和以后的版本里，可以直接从协程里返回值 `return response.bdoy`.


## 协程

tornado 中写异步代码，协程是推荐的使用方式。协程使用 `yield` 关键字用于挂起和回复程序的执行，而不是使用回调链的方式。在 tornado 里所有的协程都使用显式的上下文切换， tornado 里的协程也叫做异步函数。


### python 3.5：async and await

python 3.5 引入了 async 和 await 关键字，使用这两个关键字的函数也叫做原生协程。从 tornado 4.3 起，可以使用这两个关键字替换绝大多数基于 `yield` 的协程，不过，The await keyword is less versatile than the yield keyword：

- 在一个基于 yield 的协程里，可以 yield 一个由 Future 对象组成的列表，但当使用原生协程时必须把这个列表用 `tornado.gen.multi` 进行包裹
- 使用原生协程时不能与 `concurrent.futures` 进行集成

使用 `async` 和 `await` 也会比使用 `yield` 更快：

```python
async def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body
```

We can use `tornado.gen.convert_yielded` to convert anything that would work with yield into a form that will work with await:

```python
async def f():
    executor = concurrent.futures.ThreadPoolExecutor()
    await tornado.gen.convert_yielded(executor.sumbit(g))
```

### how it works

`@gen.coroutine` 装饰器通过 `yield` 表达式与生成器进行通信，并给协程的调用者返回一个 `Future` 对象。

下面是简化版的协程装饰器内部循环：

```python
# tornado.gen.Runner 里内部循环的简化版
def run(self):
    future = self.gen.send(self.next)
    def callback(f):
        self.next = f.result()  # unwrap
        self.run()  # loop
    future.add_done_callback(callback)

```

装饰器从生成器里接收一个 `Future` 对象，然后等待（非阻塞）这个 future 完成，然后 "unwraps" 这个 `Future` 对象，并把这个 future 返回的结果发送回生成器（作为生成器 `yield` 表达式的值）。 绝大多数异步程序不会直接使用 `Future` 这个类里，除了将由异步函数返回的 `Future` 对象立即传递给 `yield` 表达式。

### how to call a coroutine

Coroutines do not raise exceptions in the normal way: any exception they raise will be trapped in the `Future` until it is yielded. 这意味着以正确的方式调用协程是很重要的，否则我们可能不会注意到是哪里发生了错误：

```python
@gen.coroutine
def divide(x, y):
    return x / y

def bad_call():
    # this should raise a ZeroDivisionError
    # but it won't
    divide(1, 0)
```

基本上在所有情况下，一个调用协程的函数，其自身也必须是协程，并在调用协程时使用 `yield` 关键字。当覆写父类中的方法时，需要查看文档是否允许使用协程。

```python
@gen.coroutine
def good_call():
    # yield will unwrap the Future returned by divide()
    # and raise the exeception
    yield divide(1, 0)
```

有时我们需要 fire and forget” a coroutine without waiting for its result，这时可以使用 `IOLoop.spawn_callback`，让 `IOLoop` 负责这个协程的调用，如果这个协程运行失败了， `IOLoop` 会将调用栈进行 log 输出：

```python
IOLoop.current().spaqn_callback(divide, 1, 0)
```

对于使用 `@gen.coroutine` 的函数推荐使用 `IOLoop.spawn_callback` 完成这种需求，而对于原生协程（使用 `async def`）则必须使用 `IOLoop.spawn_callback` 来完成。

最后，在程序的最高层级，如果 `IOLoop` 还没有运行。我们可以开启它，然后运行协程，还可以使用 `IOLoop.run_sync` 方法终止 `IOLoop`。

```python
# run_sync() doesn't take argumets,
# so we must wrap the call in a lambda
IOLoop.current().run_sync(lambda: divide(1, 0))
```

### coroutine patterns

#### 在协程里调用阻塞函数

在协程里调用一个阻塞函数最简单的方法是使用 `IOLoop.run_in_executor`，这会返回一个与协程相兼容的 `Future` 对象：

```python
@gen.coroutine
def call_blocking():
    yield IOLoop.current().run_in_executor(blocking_func, args)
```

#### 并行处理

tornado 的协程装饰器可以识别值为 `Future` 对象的列表和字典，可以并行的等待这些 future 完成：

```python
@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]

@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]
    # responses is a list of HTTPResponses in the same order

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                        for url in urls}
    # responses is a dict {url: HTTPResponse}
```

当使用  `await` 时，列表和字典必须使用 `tornado.gen.multi` 进行包裹一下：

```python
async def parallel_fetch(url1, url2):
    resp1, resp2 = await gen.multi([http_client.fetch(url1),
                                    http_client.fetch(url2)])
```

#### 混合 （Interleaving）

有时可能需要保存一个 `Future` 对象，而不是立刻要 yield 出来，然后可以进行其他的操作：

```python
@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()
```

这个模式最适合结合 `@gen.coroutine` 使用，如果 `fetch_next_chunk()` 使用 `async def`，必须要这样调用：

 `fetch_future = tornado.gen.convert_yielded(self.fetch_next_chunk())`

 以便在后台开启协程。

 #### 循环

使用原生协程时，可以使用 `async for`。而如果使用老版本的 python，我们需要 separate the loop condition from accessing the results，下面是一个使用 `Motor` 的例子：

```python
import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next()):
        doc = cursor.next_object()
```

 #### 后台运行

协程不常使用 `PeriodicCallback`，不过协程里可以使用 `while True:` 循环和 `tornado.gen.sleep`:

```python
@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)

# coroutines that loop forever are generally started with spawn_callback()
IOLoop.current().spawn_callback(minute_loop)
```

上面的代码会每 `60 + N` 秒循环一次，为了实现每次循环正好用时 60 秒，可以做一下处理：

```python
@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)  # start the clock
        yield do_something()  # run while the clock is ticking
        yield nxt  # wait for the timer to run out
```


##  Queue example - 一个并发的网络爬虫

Tornado 的 `tornado.queues` 模块，模拟标准库中用于实现线程的生产者/消费者模型的 `queue` 模块，实现了一个用于协程的异步生产者/消费者模型。

 当一个协程在产出 `Queue.get` 时会暂停，直到队列里有东西时为止。如果队列已满，当一个协程在产出 `Queue.put` 时会暂停，直到队列里有空间为止。

 一个 `Queue` 维护着一定数目未完成的任务，which begins at zero. `put` increments the count; `task_done` decrements it.



## tornado 网络应用的例子


## 模板与 UI


## 认证与安全


## 运行与部署



