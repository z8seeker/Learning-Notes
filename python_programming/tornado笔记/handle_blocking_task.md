```python
#!/usr/bin/env python
# encoding=utf-8

"""
recommended method to handle blocking tasks in Tornado

A ThreadPoolExecutor is the recommended way to use blocking functions that cannot be easily rewritten as non-blocking

Thread pools should generally be either global or class variables; not instance variables.
It is a good practice to have one thread pool for each kind of resource: e.g. one thread pool for database queries and
second pool for image processing. This lets you set and monitor separate limits for each one.

Notice:
Browsers will generally not let you make more than one request at a time to the same url. If you use different urls in
firefox you should see multiple requests at once (but only a few requests at a time to a given domain)

"""

import tornado.web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import coroutine
import time


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world %s" % time.time())


class SleepHandler(tornado.web.RequestHandler):
    @property
    def executor(self):
        return self.application.executor

    @coroutine
    def get(self, n):
        n = yield self._long_time_task(n)
        self.write("Awake! %s" % time.time())
        self.finish()

    @run_on_executor
    def _long_time_task(self, n):
        """
        This is a long time job and may block the server,such as a complex DB query or Http request.
        """
        time.sleep(float(n))
        return n


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
                        (r"/", MainHandler),
                        (r"/sleep/(\d+)", SleepHandler),
                    ]
        tornado.web.Application.__init__(self, handlers)
        self.executor = ThreadPoolExecutor(max_workers=10)


if __name__ == "__main__":
    application = App()
    application.listen(8810)
    tornado.ioloop.IOLoop.instance().start()

```