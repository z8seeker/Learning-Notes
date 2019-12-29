# Nginx 配置

nginx 的配置文件是以块（block）的形式组织的，每个块以一个花括号（{}）来表示，主要有六种块：

- main, 全局配置，在配置的最顶层，包含 events block 和 http block
- events, 事件配置，控制 nginx 处理连接的方式
- http, http 配置，包含 server block 和 upstream block
- server, 主机配置，包含多个 location block
- upstream, 负载均衡配置
- location，url 模式配置

## upstream block

### nginx 支持的负载均衡算法

nginx 的负载均衡模块目前支持 4 种调度算法：

- round-robin, 默认的轮询算法
- least_conn, 请求会被发送到活跃连接数最少的服务器上
- ip_hash, 根据访问 ip 的哈希结果分配请求
- hash, 根据某个键的哈希结果分配请求

```bash
# least_conn
upstream backend {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

# ip_hash
upstream backend {
    ip_hash;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

# hash
upstream backend {
    hash $request_uri; # 根据请求地址生成哈希结果
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}
```

### 负载均衡支持的状态参数

upstream 模块中支持四种状态类型：

- down, 当前的服务器暂不参与负载均衡
- max_fails, 允许请求失败的次数，默认为 1
- fail_timeout, 在经历了 max_fails 次失败后，暂停服务的时间，默认为 10s
- backup, 预留的备份服务器

## location block


## max_fails 与 fail_timeout

今天在下面的这个 NGINX 例子配置文件里里看到一个有意思的观点，就是如果后端是一个动态程序，那么 upstream 的 fail_timeout 应该设置为 0 ：

https://bogomips.org/unicorn/examples/nginx.conf

```c
upstream app_server {
  ...
  server 192.168.0.7:8080 fail_timeout=0;
  ...
}
```

`fail_timeout` 的默认值是 10 秒，配合默认值为 1 的 `max_fails` 参数，意思是如果在 `fail_timeout` 期间后端失败了 `max_fails` 次，那么就将这个后端标识为不可用，在接下来的 `fail_timeout` 期间， NGINX 不会再将请求分配到这个后端。

如果将 `fail_timeout` 设置为 0 ，那么无论后端失败了多少次， NGINX 会继续把请求分发到这个后端服务器地址。

如果后端是一个动态程序，比如 Python 或者 Node.js ，那么就应该将 `fail_timeout` 设置为 0 ，这样即使后端偶尔抛出一个 500 错误，那么也不应该暂停服务。在动态应用中，出现偶尔的 500 错误是很正常而且几乎无法避免的。如果后端因为某些更严重的原因一直出现 500 错误，那么这种问题其实也是任何 NGINX 配置都解救不了的。

`fail_timeout` 设置为 10 秒或者更长时间，可能对于静态的后端会更有意义。因为静态的后端通常很难出现 500 错误。如果出错了，一般也都是因为一些更麻烦的问题，比如硬盘坏了，或者内存满了之类，这种时候通过 `fail_timeout` 的值来暂时避免将请求发送到有问题的静态后端，是有意义的。

默认：`fail_timeout` 为10s, `max_fails` 为1次。

Nginx基于连接探测，如果发现后端异常，在单位周期为 `fail_timeout` 设置的时间，中达到 `max_fails` 次数，这个周期次数内，如果后端同一个节点不可用，那么接将把节点标记为不可用，并等待下一个周期（同样时常为 `fail_timeout` ）再一次去请求，判断是否连接是否成功。如果成功，将恢复之前的轮询方式，如果不可用将在下一个周期( `fail_timeout` )再试一次。

有的时候情况是这样的，后端其实还有处理能力，但是因为 `fail_timeout` 和 `max_fails` 的值不理想，而被浪费了。这也是为什么有时候后端明明还活着，但是错误日志里却出现 no live upstreams while connecting to upstream 。
