# interface

接口是一种抽象类型，它定义了一组字段。为了实现这个接口，相应的类型必须包括这些字段。Go 通过 interface 实现了 `duck-typing`。

空 interface（interface{}）不包含任何的 method，所有的类型都实现了空 interface，所以空 interface 可以存储任意类型的数值，这有点类似于 C 语言中的 `void*` 类型：

```go
// a 为空接口
var a interface{}
var i int = 5
s := "Hello world"
// a 可以存储任意类型的值
a = i
a = s
```

一个函数把 interface{} 作为参数，那么他可以接受任意类型的值作为参数，如果一个函数返回 interface{},那么也就可以返回任意类型的值。

## interface 函数参数


## interface 变量存储的类型

- `Comma-ok` 断言。`value, ok = element.(T)`, element 是 interface 变量， T 是断言的类型。
- `switch` 测试。使用 `element.(type)` 语法

## 嵌入 interface

如果一个 interface1 作为 interface2 的一个嵌入字段，那么 interface2 隐式的包含了 interface1 里面的 method。

## 反射

反射就是能检查程序在运行时的状态，用到的包是 reflect:

```go
t := reflect.TypeOf(i)  // 得到类型的元信息
v := reflect.ValueOf(i)  // 得到实际的值
```
