# 流程和函数

Go中流程控制分三大类：条件判断，循环控制和无条件跳转。

## 条件判断

### if

Go 里面 if 条件判断语句中不需要括号，此外条件判断语句里面允许声明一个变量，这个变量的作用域只能在该条件逻辑块内，其他地方就不起作用了：

```go
if x > 10 {
    fmt.Println("x is greater than 10")
} else {
    fmt.Println("x is less than 10")
}

// 计算获取值x,然后根据x返回的大小，判断是否大于10
if x := computedValue(); x > 10 {
    fmt.Println("x is greater than "10")
} else {
    fmt.Println("x is less than 10")
}

fmt.Println(x)  // 编译出错，因为 x 是条件里面的变量

if integer == 3 {
    fmt.Println("The integer is equal to 3")
} else if integer < 3 {
    fmt.Println("The integer is less than 3")
} else {
    fmt.Println("The integer is greater than 3")
}
```

## 跳转

### goto

用 goto 跳转到必须在当前函数内定义的标签：

```go
func myFunc() {
    i := 0
Here:  // 这行的第一个词，以冒号结束作为标签
    println(i)
    i++
    goto Here  // 跳转到 Here 去
}
```

## 循环控制
