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


