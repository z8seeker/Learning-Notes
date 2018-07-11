# tornado 异步网络服务

阅读 introducing to torando






使用 tornado.httpclient 发送请求，会返回一个 HTTPResponse 对象。

AsyncHTTPClient 的 fetch 方法，可以指定一个 callback 参数，当请求完成后会调用这个 callback 函数, 并将 HTTPResponse 对象作为参数传入这个 callback。



