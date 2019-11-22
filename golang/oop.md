# oop

A method is a function with an implict first argument, called a receiver.

method 的语法如下：

```go
func (r ReceiverType) funcName(parameters) (results)
```

在使用 method 的时候需要注意：

- 即使 method 的名字相同，但如果接收者不一样，那么 method 就不一样
- method 里可以访问接收者的字段
- 调用 method 通过 `.` 访问

method 的 Receiver 既可以值传递，也可以是指针。指针作为 Receiver 会对实例对象的内容进行操作。

method 可以用在任何自定义类型，内置类型，struct 等各种类型上面。

```go
type ages int

type money float32

type months map[string]int

m := months {
    "January": 31,
    "February": 28,
}
```

## method 继承

如果匿名字段实现了一个 method，那么包含这个匿名字段的 struct 也能调用该 method。

## method 重写

可以重写匿名字段的方法。

Go里面的面向对象，没有任何的私有、公有关键字，通过大小写来实现(大写开头的为公有，小写开头的为私有)，方法也同样适用这个原则。

## 类型和接口

在 Go 中，接口和类型可以直接转换，甚至接口的定义都不用在类型定义之前。
