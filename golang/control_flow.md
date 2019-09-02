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

### switch

switch 语法格式如下：

```go
switch sExpr {
case expr1:
	some instructions
case expr2:
	some other instructions
case expr3:
	some other instructions
default:
	other code
}
```

`sExpr` 和 `expr1`、`expr2`、`expr3` 的类型必须一致。执行的过程从上至下，直到找到匹配项；而如果 `switch` 没有表达式，它会匹配 `true`。

Go 里面 `switch` 默认相当于每个 `case` 最后带有 `break`，匹配成功后不会自动向下执行其他 `case`，而是跳出整个 `switch`, 但是可以使用 `fallthrough` 强制执行后面的 `case` 代码

```go
i := 10
switch i {
    case 1:
        fmt.Println("i is equal to 1")
    case 2, 3, 4:
        fmt.Println("i is equal to 2, 3 or 4")
    case 5:
        fmt.Println("The integer was <= 5")
        fallthrough
    case 10:
        fmt.Println("i is equal to 10")
    default:
        fmt.Println("default case")
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

### for

Go 里面最强大的一个控制逻辑就是 for，它既可以用来循环读取数据，又可以当作 while 来控制逻辑，还能迭代操作:

```go
package main

import "fmt"

func main() {
    sum := 0
    for index:=0; index < 10; index++ {
        sum += index
    }
    fmt.Println("sum is equal to ", sum)
}
// 输出：sum is equal to 45
```

for 语句的简化版本：

```go
// 忽略 expression1 和 expression3
sum := 1
for ; sum < 1000; {
    sum += sum
}
// 还可以继续省略 ;
sum := 1
for sum < 1000 {
    sum += sum
}
```

在循环里面有两个关键操作 `break` 和 `continue`, `break` 操作是跳出当前循环，`continue` 是跳过本次循环:

```go
for index := 10; index > 0; index-- {
    if index == 5 {
        break  // 或者 continue
    }
    fmt.Println(index)
}
```

当嵌套过深的时候，`break` 可以配合标签使用，即跳转至标签所指定的位置。`break` 和 `continue` 还可以跟着标号，用来跳到多重循环中的外层循环。

`for` 配合 `range` 可以用于读取 `slice` 和 `map` 的数据：

```go
for k, v := range map {
    fmt.Println("map's key:", k)
    fmt.Println("map's val:", v)
}
```

## 函数

函数是 Go 里面的核心设计，它通过关键字 `func` 来声明，语法格式如下：

```go
func funcName(input1 type1, input2 type2) (output1 type1, output2 type2) {
	//这里是处理逻辑代码
	//返回多个值
	return value1, value2
}
```

- 关键字 `func` 用来声明一个函数 `funcName`
- 函数可以有一个或者多个参数，每个参数后面带有类型，通过 `,` 分隔
- 函数可以返回多个值
- 上面返回值声明了两个变量 `output1` 和 `output2`，如果你不想声明也可以，直接就两个类型
- 如果只有一个返回值且不声明返回值变量，那么你可以省略 包括返回值 的括号
- 如果没有返回值，那么就直接省略最后的返回信息
- 如果有返回值， 那么必须在函数的外层添加 `return` 语句

使用函数：

```go
package main

import "fmt"

// 返回 a, b 中的最大值
func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

// 多个返回值
func sumAndProduct(A, B int) (int, int) {
    return A+B, A*B
}

// 命名返回参数的变量
func SumAndProduct(A, B int) (add int, Multiplied int) {
    add = A+B
    Multiplied = A*B
    return  // 因为直接在函数里面初始化了, 返回的时候不用带上变量名
}
```

### 变参

接受变参的函数是有着不定数量的参数的。为了做到这点，首先需要定义函数使其接受变参：

```go
func myfunc(arg ...int) {
    for _, n := range arg {
        fmt.Printf("And the number is: %d\n", n)
    }
}
```

在函数体中，变量 `arg` 是一个 `int` 的 `slice`。

### 传值与传指针

当我们传一个参数值到被调用函数里面时，实际上是传了这个值的一份 copy，当在被调用函数中修改参数值的时候，调用函数中相应实参不会发生任何变化，因为数值变化只作用在 copy 上。

```go
package main

import "fmt"

// 传值
func add1(a int) int {
    a = a + 1
    return a
}

// 传指针
func add2(a *int) int {
    *a = *a + 1
    return *a
}
```

传值与传指针的区别：

- 传指针使得多个函数能操作同一个对象。
- 传指针比较轻量级 (8 bytes),只是传内存地址，我们可以用指针传递体积大的结构体。如果用参数值传递的话, 在每次 copy 上面就会花费相对较多的系统开销（内存和时间）。所以当你要传递大的结构体的时候，用指针是一个明智的选择。
- Go 语言中 `channel`，`slice`，`map` 这三种类型的实现机制类似指针，所以可以直接传递，而不用取地址后传递指针。（注：若函数需改变 `slice` 的长度，则仍需要取地址传递指针）

### defer

可以在函数中添加多个 `defer` 语句。当函数执行到最后时，这些 `defer` 语句会按照逆序执行，最后该函数返回:

```go
// 返回前关闭相应的资源
func ReadWrite() bool {
    file.Open("file")
    defer file.Close()
    if failureX {
        return false
    }
    if failureY {
        return false
    }
    return true
}

// 多个 defer 调用，后进先出
for i := 0; i < 5; i++ {
    defer fmt.Printf("%d ", i)
}  // 输出：4 3 2 1 0
```

### 函数作为值/类型

在 Go 中函数也是一种变量，我们可以通过 type 来定义它，它的类型就是所有拥有相同的参数，相同的返回值的一种类型：

```go
type typeName func(input1 inputType1 , input2 inputType2 [, ...]) (result1 resultType1 [, ...])
```

函数当做值和类型在我们写一些通用接口的时候非常有用，可以使得我们的程序变得非常的灵活：

```go
package main

import "fmt"

type testInt func(int) bool  // 声明了一个函数类型

func isOdd(integer int) bool {
    if integer%2 == 0 {
        return false
    }
    return true
}

func isEven(integer int) bool {
    if integer%2 == 0 {
        return true
    }
    return false
}

func filter(slice []int, f testInt) []int {
    var result []int
    for _, value := range slice {
        if f(value) {
            result = append(result, value)
        }
    }
    return result
}

func main(){
    slice := []int {1, 2, 3, 4, 5, 7}
    fmt.Println("slice = ", slice)
    odd := filter(slice, isOdd)  // 函数当做一个值来传递
    fmt.Println("Odd elements of slice are: ", odd)
    even := filter(slice, isEven)  // 函数当做一个值来传递
    fmt.Println("Even elements of slice are: ", even)
}
```

### Panic 和 Recover

Go 没有像 Java 那样的异常机制，它不能抛出异常，而是使用了 `panic` 和 `recover` 机制。

Panic

```
内建函数，可以中断原有的控制流程，进入一个 panic 状态中。当函数 F 调用 panic，函数 F 的执行被中断，但是 F 中的延迟函数会正常执行，然后 F 返回到调用它的地方。在调用的地方，F 的行为就像调用了 panic。这一过程继续向上，直到发生 panic 的 goroutine 中所有调用的函数返回，此时程序退出。panic 可以直接调用 panic 产生。也可以由运行时错误产生，例如访问越界的数组。
```

Recover

```
内建的函数，可以让进入 panic 状态的 goroutine 恢复过来。recover 仅在延迟函数中有效。在正常的执行过程中，调用 recover 会返回 nil，并且没有其它任何效果。如果当前的 goroutine 陷入 panic 状态，调用 recover 可以捕获到 panic 的输入值，并且恢复正常的执行。
```

```go
var user = os.Getenv("USER")
// 使用 panic
func init() {
    if user == "" {
        panic("no value for $USER")
    }
}

// 使用 recover

func throwsPanic(f func()) (b bool) {
    defer func() {
        if x := recover(); x != nil {
            b = true
        }
    }()
    f()  // 执行函数 f
    return
}
```

### main 函数和 init 函数

Go 里面有两个保留的函数：`init` 函数（能够应用于所有的 package）和 `main` 函数（只能应用于 `package main`）。这两个函数在定义时不能有任何的参数和返回值。

Go 程序会自动调用 `init()` 和 `main()`，所以你不需要在任何地方调用这两个函数。每个package中的 `init` 函数都是可选的，但 `package main` 就必须包含一个 `main` 函数。

程序的初始化和执行都起始于 main 包。如果 main 包还导入了其它的包，那么就会在编译时将它们依次导入。有时一个包会被多个包同时导入，那么它只会被导入一次。

当一个包被导入时，如果该包还导入了其它的包，那么会先将其它包导入进来，然后再对这些包中的包级常量和变量进行初始化，接着执行 `init` 函数（如果有的话），依次类推。等所有被导入的包都加载完毕了，就会开始对 main 包中的包级常量和变量进行初始化，然后执行 main 包中的 `init` 函数（如果存在的话），最后执行 `main` 函数。

### import

使用 import 命令来导入包文件：

```go
// 导入标准库中的包，在 GOROOT 环境变量指定目录下加载该模块
import(
    "fmt"
)

// 相对导入，当前文件同一目录
import "./model"

// 绝对导入，加载 gopath/src/..
import "shorturl/model"

// 点操作
// 调用这个包的函数时，可以省略前缀的包名
import(
    . "fmt"
)

// 别名操作
// 把包命名成另一个我们用起来容易记忆的名字
import(
    f "fmt"
)

// _ 操作
// 引入该包，而不直接使用包里面的函数，而是调用了该包里面的 init 函数
import (
    "database/sql"
    _ "github.com/ziutek/mymysql/godrv"
)
```
