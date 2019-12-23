# Data Types

Go’s types fall into four categories: 

- basic types. int, float, complex, rune, string, bool
- aggregate types. arrays, structs
- reference types, 
- and interface types.

## 值语义与引用语义

值语义与引用语义的差别在于赋值：

```go
b = a
b.Modify()
```

若 b 的修改不会影响 a 的值，那么此类型属于值类型，否则属于引用类型。Go 语言中的大多数类型都基于值语义，包括：

- 基本类型， 如 byte, int, bool, float32, float64, string 等
- 复合类型，如 array， struct， pointer 等

Go 语言中有四个类型比较特别，看起来像引用类型：

- slice，指向数组的一个区间
- map，本质上一个字典指针
- channel， 本质上是一个指针
- interface，本质上是内部维持了两个指针

