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

 ## struct 的匿名字段

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

 struct 组合时，如果外层和内层有同名字段， go 会优先访问最外层的，这就允许我们去重载通过匿名字段继承的一些字段。
 