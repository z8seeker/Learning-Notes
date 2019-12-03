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

method 可以用在任何自定义类型，内置类型，struct 等各种类型上面（但不包括指针类型）。

```go
type ages int

type money float32

type months map[string]int

m := months {
    "January": 31,
    "February": 28,
}

type Rect struct {
    x, y float64
    width, height float64
}

func (r, *Rect) Area() float64 {
    return r.width * r.height
}

rect1 := new(Rect)
rect2 := &Rect{}
rect3 := &Rect{0, 0, 100, 200}
rect4 := &Rect{width: 100, height: 200}
```

## method 继承 (匿名组合)

如果匿名字段实现了一个 method，那么包含这个匿名字段的 struct 也能调用该 method。

```go
type Base struct {
    Name string
}
type Foo struct {
    Base
    // ...
}

// 还可以以指针方式从一个类型派生
type Foo struct {
    *Base
    // ...
}
```

## method 重写

可以重写匿名字段的方法。

Go里面的面向对象，没有任何的私有、公有关键字，通过大小写来实现(大写开头的为公有，小写开头的为私有)，方法也同样适用这个原则。

名字冲突问题：

```go
type Logger struct {
    Level int
}

type Y struct {
    *Logger
    Name string
    *log.Logger  // 匿名组合类型相当于以其类型名称（去掉包名部分），作为成员变量的名字
}
```

此时， Y 类型中存在两个名为 Logger 的成员，出现名字冲突。假如这两个 Logger 在定义后再也没被用过，那么编译器将忽略掉这个冲突问题。

## 可见性

要使某个符号对于其他包可见，需要将该定义为以大写字母开头。Go 语言中符号的可见性是包一级的而不是类型一级的。

## 类型和接口

在 Go 中，接口和类型可以直接转换，甚至接口的定义都不用在类型定义之前。

一个类只需要实现了接口要求的所有函数，就认为这个类实现了该接口，Go 语言的接口是非侵入式的：

```go
// 定义一个 File 类
type File struct {
    // ...
}
// 实现有 Read(), Write(), Seek(), Close() 方法
func (f *File) Read(buf []byte) (n int, err error)
func (f *File) Write(buf []byte) (n int, err error)
func (f *File) Seek(off int64, whence int) (pos int64, err error)
func (f *File) Close() error

// 设想我们有如下接口
type IFile interface {
    Read(buf []byte) (n int, err error)
    Write(buf []byte) (n int, err error)
    Seek(off int64, whence int) (pos int64, err error)
    Close() error
}

type IReader interface {
    Read(buf []bytes) (n int, err error)
}

type IWriter interface {
    Write(buf []bytes) (n int, err error)
}

type IClose interface {
    Close() error
}

// 虽然 File 类没有从这些接口继承，但因为实现了这些接口，可以直接进行赋值
var file1 IFile = new(File)
var file2 IReader = new(File)
var file3 IWriter = new(File)
var file4 IClose = new(File)
```

### 接口赋值

接口赋值，分为两种情况：

- 将对象实例赋值给接口
- 将一个接口赋值给另一个接口

在 Go 中，只要两个接口拥有相同的方法列表（次序无关紧要），那么它们就是等同的，可以相互赋值。

接口赋值并不要求两个接口必须等价，只要有包含关系，子集接口就可以赋值给另一个接口。

### 接口查询

接口查询，接口查询是否成功要在运行期才能确定。

在 Go 语言中，可以询问接口指向的对象是否是某个类型：

```go
var file1 Writer = ...
// file1 指向的对象实例是否是 *File 类型
if file6, ok := file1.(*File); ok {
    // ...
}
```

### 类型查询

查询接口指向的对象实例的类型：

```go
var v1 interface{} = ...
switch v := v1.(type) {
    case int:  // 为 int 类型时
    case string:  // 为 string 类型时
    // ...
}
```

### 接口组合

可以认为接口组合是类型匿名组合的一个特定场景，只是接口只包含方法，而不包含任何成员变量。


### Any 类型

Go 语言中的任何对象实例都实现了 `interface{}` 空接口，所以 `interface{}` 是可以指向任何对象的 Any 类型。我们刚开始对其一无所知，但可以通过接口查询和类型查询逐步了解它。
