# 并发

Go 从语言层面就支持了并行。

## goroutine

goroutine 是通过 Go 的 runtime 管理的一个线程管理器：

```go
go hello(a, b, c)
```

`runtime.Gosched()` 表示让 CPU 把时间片让给别人,下次某个时候继续恢复执行该 goroutine。

`runtime.GOMAXPROCS(n)` 告诉调度器同时使用多个线程。GOMAXPROCS 设置了同时运行逻辑代码的系统线程的最大数量，并返回之前的设置。如果 n < 1，则不会改变当前设置。

使用 goroutine 有一个设计原则：不要通过共享来通信，而要通过通信来共享。

## channels

goroutine 运行在相同的地址空间，访问共享内存必须做好同步。goroutine 之间进行数据通信的机制是 channel。在定义一个 channel 时，也需要定义发送到 channel 的值的类型：

```go
ci := make(chan int)
cs := make(chan string)
cf := make(chan interface{})
```

channel 通过 `<-` 来接收和发送数据：

```go
ch <- v  // 发送 v 到 channel ch
v := <-ch  // 从 ch 中接收数据，并赋值给 v
```

默认情况下， channel 接收和发送数据都是阻塞的，除非另一端已经准备好。

## Buffered Channels

Go 允许指定 channel 的缓冲大小，也就是 channel 可以存储多少元素：

```go
ch := make(chan type, value)
```

## Range 和 Close

可以通过 Range 操作缓存类型的 channel。

应该在生产者的地方关闭 channel，而不是消费的地方。

## Select

当存在多个 channel 时，通过 `select` 可以监听 channel 上的数据流动。

`select` 默认是阻塞的，只有当监听的 channel 中有发送或接收可以进行时才会运行，当多个 channel 都准备好的时候，select 是随机的选择一个执行的。

在 select 里面还有 default 语法，select 其实就是类似 switch 的功能，default 就是当监听的 channel 都没有准备好的时候，默认执行的（select 不再阻塞等待 channel）

可以用 select 来设置超时，避免整个程序进入阻塞的状态

## runtime goroutine

runtime 包中有几个处理 goroutine 的函数：

- `Goexit`
- `Gosched`，让出当前 goroutine 的执行权限
- `NumCPU`， 返回 CPU 核数量
- `NumGoroutine`，返回正在执行和排队的任务总数
- `GOMAXPROCS`，用来设置可以并行计算的 CPU 核数的最大值，并返回之前的值。

