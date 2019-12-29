# struct 类型

Go语言中，我们可以声明新的类型，作为其它类型的属性或字段的容器，这样的类型称之为 `struct`:

 ```go
// 定义 struct
type person struct {
    name string
    age int
}

// 使用
var P person
P.name = "Astaxie"
P.age = 25
fmt.Printf("The person's name is %s", P.name)
 ```

 ## 访问字段

 使用 `.` 可以访问结构体类型中的字段，或为字段赋值。使用 `&` 对字段进行取地址操作。

 ## 结构体指针

 结构体与数组一样，都是值传递。为了提高性能，可以使用结构体指针，即一个指向结构体的指针。

 使用 Go 内置 `new()` 函数，可以分配内存来初始化结构体，并返回分配的内存指针。

## 字段可见性

定义结构体时如果字段名首字母是小写的，这意味着这些字段在包外不可见，因而无法在其他包中被访问，只允许包内访问。如果想在一个包中访问另一个包中结构体的字段，则必须是大写字母开头的变量。

## Tags

在定义结构体字段时，除字段名称和数据类型外，还可以使用 __反引号__ 为结构体字段声明元信息，这种元信息称为 `Tag`，Go 会在编译阶段将其关联到字段当中

## 方法

将函数绑定到具体的类型中，则称该函数是该类型的方法，其定义的方式是在 func 与函数名称之间加上具体类型变量，这个类型变量称为 __方法接收器__:

```go
func setName(m Member,name string){//普通函数
    m.Name = name
}

func (m *Member)setName(name string){//绑定到Member结构体的方法
    m.Name = name
}
```

## 组合

一个结构体中，其字段可以是其他的结构体，这样，不同的结构体就可以共用相同的字段

 ## 匿名字段

 在定义 struct 的时候，Go 支持只提供类型而不写字段名的方式，也就是匿名字段。当匿名字段也是一个 struct 时， 这个 struct 所拥有的全部字段都被隐式地引入了当前定义的这个 struct：

 ```go
package main

import "fmt"

type Human struct {
    name string
    age int
    weight int
}

type Student struct {
    Human
    speciality string
}

func main() {
    mark := Studnet{Human{"Mark",  25, 120}, "Computer Science"}
    mark.name
    mark.age
    mark.weight
    mark.speciality

    mark.Human = Human{"Marcus", 55, 220}
    mark.Human.age -= 1
}
 ```

通过匿名字段组合其他类型，而后访问匿名字段类型所带的方法和字段时，不需要使用叶子属性，非常方便。

struct 组合时，如果外层和内层有同名字段， go 会优先访问最外层的，这就允许我们去重载通过匿名字段继承的一些字段。
 