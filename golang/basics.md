# 基础

每一个可独立运行的 Go 程序，必定包含一个 package main，在这个 main 包中必定包含一个入口函数 main，而这个函数既没有参数，也没有返回值。

我们通过关键字 func 定义了一个 main 函数，函数体被放在 {}（大括号）中，就像我们平时写 C、C++或Java时一样。

go 的包名和包所在的文件夹名可以是不同的。Go是天生支持 UTF-8 的，任何字符都可以直接输出，你甚至可以用 UTF-8 中的任何字符作为标识符。

## 变量/常量/内置类型

### 定义变量

使用 var 关键字是 Go 最基本的定义变量方式：

```go
//定义一个名称为“variableName”，类型为"type"的变量
var variableName type

// 定义三个类型都是 "type" 的变量
var vname1, vname2, vname3 type

// 定义变量并初始化
var variableName type = value

// 同时初始化多个变量
var vname1, vname2, vname3 type = v1, v2, v3

// 简化版本1
var vname1, vname2, vname3 = v1, v2, v3

// 简化版本2
vname1, vname2, vname3 := v1, v2, v3
```

`:=` 这个符号直接取代了 var 和 type,这种形式叫做简短声明。不过它有一个限制，那就是它只能用在 _函数内部_；在函数外部使用则会无法编译通过，所以一般用 var 方式来定义全局变量。

`_`（下划线）是个特殊的变量名，任何赋予它的值都会被丢弃:

```go
// 将值 35 赋值给 b，同时丢弃 34
_, b := 34, 35
```

Go 对于已声明但未使用的变量会在编译阶段报错。

### 常量

常量，也就是在程序编译阶段就确定下来的值，而程序在运行时无法改变该值。常量可定义为数值、布尔值或字符串等类型：

```go
const constantName = value
// 也可以指定常量的类型
const Pi float32 = 3.1415926
```

### 内置基础类型

#### 布尔类型

在Go中，布尔值的类型为 bool，值是 true 或 false，默认为 false

```go
var isActive bool  // 全局变量声明
var enabled, disabled = true, false  // 忽略类型的声明
func test() {
    var available bool
    valid := false
    available = true
}
```

布尔类型不能接受其他类型的赋值，不支持自动或强制的类型转换。

#### 数值类型

整数类型有无符号和带符号两种。Go 同时支持 int 和 uint，这两种类型的长度相同。Go 里面也有直接定义好位数的类型：`rune`, `int8`, `int16`, `int32`, `int64` 和 `byte`, `uint8`, `uint16`, `uint32`, `uint64`。其中 `rune` 是 `int32` 的别称，`byte` 是 `uint8` 的别称。

需要注意的一点是，这些类型的变量之间不允许互相赋值或操作，不然会在编译时引起编译器报错。但各种类型的整型变量都可以直接与字面常量（literal）进行比较。

浮点数的类型有 `float32` 和 `float64` 两种（没有 `float` 类型），默认是 `float64`。

Go 还支持复数。它的默认类型是 `complex128`（64 位实数 + 64 位虚数）。如果需要小一些的，也有 `complex64` (32 位实数 + 32 位虚数):

```go
var c complex64 = 5 + 5i
fmt.Printf("Value is: %v", c)
```

#### 字符串

Go 中的字符串都是采用 UTF-8 字符集编码。字符串是用一对双引号（`""`）或反引号（``` ```）括起来定义，它的类型是 string:

```go
var frenchHello string
var emptyString string = ""  // 初始化为空字符串
func test() {
    no, yes, maybe := "no", "yes", "maybe"
    japaneseHello := "Konichiwa"
    frenchHello = "Bonjour"  // 常规赋值
}
```

在 Go 中字符串是不可变的：

```go
var s string = "hello"
s[0] = 'c'  // 编译时会报错：cannot assign to s[0]

// 借助 byte 间接修改字符串内容
s := "hello"
c := []byte(s)  // 将字符串转换为 []byte 类型
c[0] = 'c'
s2 := string(c)  // 再转换回 string 类型
fmt.Printf("%s\n", s2)

// 可以使用 + 操作符来连接两个字符串
s := "hello,"
m := " world"
a := s + m

// 字符串切片操作
s := "hello"
s = "c" + s[1:]
```

``` 括起的字符串为 Raw 字符串，即字符串在代码中的形式就是打印时的形式，它没有字符转义，换行也将原样输出:

```go
m := `hello
        world`
```

Raw 字符串可以方便的应用于 正则表达式、HTML 模板、JSON 字面量 等场景。


#### 字符类型

Go 支持两个字符类型：

- `byte`, 实际是 `uint8` 的别名，代表 UTF-8 字符串的单个字节的值
- `rune`, 代表单个 Unicode 字符, 其实是 int32.

UTF-8 编码

UTF-8 是一种可变长的编码方案，将 Unicode code point 编码为 bytes。UTF-8 使用 1-4 个字节来表示每个 rune：

- 使用 1 个字节表示 ASCII 字符
- 使用 2 或 3 个字节表示绝大多数 rune

The high-order bits of the first byte of the encoding, 表示有几个字节来表示该 rune:

- 0, 表示 7 位的 ASCII， 此时每个 rune 只占用一个字节 （0-127）
- 110， 表示该 rune 占用 2 个字节，且第二个字节以 10 开头 （128-2047）
- 1110，表示该 rune 占用 3 个字节，且第二个字节和第三个字节都以 10 开头 (2048-65535)
- 11110， 表示 rune 占用 4 个字节， 且第二个、第三个、第四个字节均以 10 开头 (65535-0x10ffff)

```go
"世界"
"\xe4\xb8\x96\xe7\x95\x8c" # encoded in utf-8
"\u4e16\u754c"  # unicode point
"\U00004e16\U0000754c"
```

上面三个转义序列和第一个字符串是相同的，它们都有相同的值。

A rune whose value is less than 256 may be written with a single hexadecimal escape, such as '\x41' for 'A', but for higher values,  a `\u` or `\U` escape must be used:

```go
'世'
// legal
'\u4e16'
'\U00004e16'

// illegal
'\xe4\xb8\x96'
```

Thanks to the nice properties of UTF-8, many string operations don't require decoding.

```go
func HasPrefix(s, prefix string) bool {
    return len(s) >= len(prefix) && s[: len(prefix)] == prefix
}
```

Go’s range loop, when applied to a string, performs UTF-8 decoding implicitly. 因此，为了正确的对字符串使用 range 循环，需要确保字符串是 utf-8 编码的，否则会引发错误。

A `[]rune` conversion applied to a UTF-8-encoded string returns the sequence of Unicode code points that the string encodes.

Converting an integer value to a string interprets the integer as a rune value, and yields the UTF-8 representation of that rune:

```go
fmt.Println(string(65))  // "A", not "65"
fmt.PrintLn(string(0x4eac))  // "京"
```

字符串与字节切片

Go 语言中有四个非常有用的包用来处理字符串：

- strings, 提供了用于 搜索、替换、比较、修剪（trimming）、切分 和 连接字符串的函数
- bytes, 提供了与 strings 包类似的功能，用于处理 `[]bytes` 类型
- strconv，布尔值、整数、浮点数与它们的字符串表示进行相互转换
- unicode，提供了 `IsDigit`, `IsLetter`, `IsUpper` 和 `IsLower` 等函数用来分类 runes

`bytes` 包中提供了 `Buffer` 类型，用于高效的处理字节切片。

When appending the UTF-8 encoding of an arbitrary rune to a `bytes.Buffer`, it's best to use `WriteRune` method, but `WriteByte` is fine for ASCII characters.


字符串与数值之间的转换

将一个整数转换为一个字符串：

- `fmt.Sprintf`
- `strconv.Itoa` (integer to ASCII)

```go
x := 123
y := fmt.Sprintf("%d", x)
fmt.Println(y, strconv.Itoa(x))
```

To parse a string representing an integer, use the strconv functions `Atoi` or `ParseInt`,or `ParseUint` for unsigned integers:

```go
x, err := strconv.Atoi("123")  // x is an int
y, err := strconv.parseInt("123", 10, 64) // base 10, up to 64 bits
```

#### 错误类型

Go 内置有一个 `error` 类型，专门用来处理错误信息，Go 的 package 里面还专门有一个包 `errors` 来处理错误:

```go
err := errors.New("emit macho dwarf: elf header corrupted")
if err != nil {
    fmt.Print(err)  # 不能使用 fmt.Printf
}
```

## 一些技巧

### 分组声明

在 Go 语言中，同时声明多个常量、变量，或者导入多个包时，可采用分组的方式进行声明：

```go
import(
    "fmt"
    "os"
)

const(
    i = 100
    pi = 3.1415
    prefix = "Go_"
)

var(
    i int
    pi float32
    prefix string
)
```

### iota 枚举

Go 里面有一个关键字 `iota`，这个关键字用来声明 `enum` 的时候采用，它默认开始值是 0，`const` 中每增加一行加 1：

```go
package main

import (
    "fmt"
)

const (
    x = iota  // x == 0
    y = iota  // y == 1
    z = iota  // z == 2
    w  // 常量声明省略值时，默认和之前一个值的字面相同。这里隐式地说w = iota，因此w == 3
)

const v = iota  // 每遇到一个 const 关键字，iota 就会重置，此时 v == 0

const (
    h, i, j = iota, iota, iota  // h=0, i=0, j=0 iota 在同一行值相同
)

const (
    a = iota  // a = 0
    b = "B"
    c = iota  // c = 2
    d, e, f = iota, iota, iota  // d=3, e=3, f=3
    g = iota  // g = 4
)

func main() {
    fmt.Println(a, b, c, d, e, f, g, h, i, j, x, y, z, w, v)
}
```

### go 程序的一些规则

- 大写字母开头的变量是可导出的，也就是其它包可以读取的，是公有变量；小写字母开头的就是不可导出的，是私有变量
- 大写字母开头的函数也是一样，相当于 `class` 中的带 `public` 关键词的公有函数；小写字母开头的就是有 `private` 关键词的私有函数


## array/slice/map

### array

`array` 就是数组，它的定义方式如下:

```go
// n 表示数组的长度，type 表示存储元素的类型
var arr [n]type

var arr[10]int  // 声明一个 int 类型的数组
arr[0] = 42  // 数组下标是从 0 开始的
arr[1] = 13  // 

// 使用 := 声明数组
a := [3]int{1, 2, 3}  // 声明一个长度为 3 的 int 数组
b := [10]int{1, 2, 3}  // 对前 3 个元素初始化，其他元素默认为 0
c := [...]int{4, 5, 6}  // 可以省略长度而采用`...`的方式，Go会自动根据元素个数来计算长度
```

由于长度也是数组类型的一部分，因此 `[3]int` 与 `[4]int` 是不同的类型，数组也就不能改变长度。在声明时长度可以为一个常量或者一个常量表达式（指在编译期即可计算结果）。可以用内置函数 `len()` 获取数组的长度。

数组之间的赋值是值的赋值，即当把一个数组作为参数传入函数的时候，传入的其实是该数组的副本，而不是它的指针。

Go支持嵌套数组，即多维数组:

```go
doubleArray := [2][4]int{[4]int{1, 2, 3, 4}, [4]int{5, 6, 7, 8}}

// 上面的声明可以简化
easyArray := [2][4]int{{1, 2, 3, 4}, {5, 6, 7, 8}}
```

使用关键字 `range` 可以方便的遍历容器中的元素：

```go
for i, v := range array {
    fmt.Println("Array element[", i, "]=", v)
}
```

__注意__：在 Go 中数组是一个值类型（value type），所有的值类型在赋值和作为参数传递时都将产生一次复制动作。

### slice

在初始定义数组时，有时我们并不知道需要多大的数组，此时需要使用“动态数组”。在Go里面这种数据结构叫 slice。

slice 总是指向一个底层 array，slice 的声明也可以像 array 一样，只是不需要长度:

```go
// 直接创建
var mySlice := make([]int, 5)  // 元素个数为 5
var mySlice := make([]int, 5, 10) // 元素个数为 5，并预留 10 个元素的存储空间

// 和声明 array 一样，只是少了长度
var fslice []int

// 初始化数据
slice := []byte {'a', 'b', 'c', 'd'}
```

slice 通过 `array[i:j]` 来获取，其中 i 是数组的开始位置，j 是结束位置，但不包含 `array[j]`，它的长度是 `j-i`

```go
// 声明一个含有 10 个元素的 byte 型数组
var ar = [10]byte {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'}

// 声明两个含有 byte 的 slice
var a, b []byte

a = ar[2:5]  // a 含有的元素： ar[2], ar[3], ar[4]

b = ar[3:5]  // b 的元素是：ar[3], ar[4]

// 更多操作
a = ar[:3]  // 包含元素 a, b, c
a = ar[5:]  // 包含元素 f, g, h, i, j
a = ar[:]  // 包含了 ar 中的全部的元素

a = ar[3:7]  // d, e, f, g, len=4, cap=7

// 基于 slice 创建新的 slice
b = a[1:3]  // e, f
b = a[:3]  // d, e, f
b = a[0:5]  // 对 slice 的 slice 可以在 cap 范围内扩展： d, e, f, g, h
b = a[:]  // d, e, f, g
```

slice 是引用类型，所以当引用改变其中元素的值时，其它的所有引用都会改变该值。从概念上面来说 slice 像一个结构体，这个结构体包含了三个元素：

- 一个指针，指向数组中 slice 指定的开始位置
- 长度，即 slice 的长度
- 最大长度（cap），也就是 slice 开始位置到数组的最后位置的长度

对于 slice 有几个有用的内置函数：

- `len()` 获取 slice 的长度
- `cap()` 获取 slice 的最大容量
- `append()` 向 slice 里面追加一个或者多个元素，然后返回一个和 slice 一样类型的 slice
- `copy()` 从源 slice 的 src 中复制元素到目标 dst，并且返回复制的元素的个数

```go
mySlice := make([]int, 5, 10)
mySlice = append(mySlice, 1, 2, 3)  // append，的第二个参数是个不定参数
mySlice2 := []int{8, 9, 10}
mySlice = append(mySlice, mySlice2...)  // 加上省略号相当于把 mySlice2 打散后传入
```

注意：

- `append` 函数会改变 `slice` 所引用的数组的内容，从而影响到引用同一数组的其它 `slice`。 但当 `slice` 中没有剩余空间（即(`cap`- `len`) == 0）时，此时将动态分配新的数组空间。返回的 `slice` 数组指针将指向这个空间，而原数组的内容将保持不变；其它引用此数组的 `slice` 则不受影响。


从 Go1.2 开始 slice 支持了三个参数的 slice:

```go
var array [10]int
Vslice := array[2:4:]  // slice 的容量是 10 - 2 = 8

new_slice := array[2:4:7]  // 容量变为 7 - 2 = 5, 无法访问最后的三个元素
```

### map

map 也就是 python 中字典的概念，是一堆键值对的未排序集合：

```go
// 定义格式
map[keyType]valueType
```

`map` 的读取和设置也类似 `slice` 一样，通过 `key` 来操作，只是 `slice` 的 `index` 只能是 `int` 类型，而 map 多了很多类型，可以是 int，可以是 string 及所有完全定义了 `==` 与 `!=` 操作的类型:

```go
// 声明一个 key 是字符串， 值为 int 的字典，
// 这种方式的声明需要在使用之前进行 make 初始化
var numbers map[string]int

// 另一种 map 的声明方式
numbers = make(map[string]int)

//在创建时，指定初始存储能力
numbers = make(map[string]int, 100)

numbers["one"] = 1  // 赋值
numbers["ten"] = 10  // 赋值
numbers["three"] = 3

fmt.Println("第三个数字是：", numbers["three"])  // 读取数据

// 初始化一个字典
rating := map[string]float32{"c": 5, "Go": 4.5, "Python": 4.5, "C++": 2}

// map 有两个返回值，
// 第二个返回值，如果不存在 key，那么 ok 为 false，如果存在, ok 为 true
csharpRating, ok := rating["C#"]
if ok {
    fmt.Println("C# is in the map and its rating is", csharpRating)
} else {
    fmt.Println("We have no rating accociated with C# in the map")
}

// 元素删除
delete(rating, "C")  // 删除 key 为 C 的元素
```

map 和其他基本型别不同，它不是 thread-safe，在多个 go-routine 存取时，必须使用 `mutex lock` 机制。

map 也是一种引用类型，如果两个 map 同时指向一个底层，那么一个改变，另一个也相应的改变：

```go
m := make(map[string]string)
m["Hello"] = "Bonjour"
m1 := m
m1["Hello"] = "Salut"
```

#### make/new 操作

`make` 用于内建类型（`map`、`slice` 和 `channel`）的内存分配。`new` 用于各种类型的内存分配。

内建函数 `new` 本质上说跟其它语言中的同名函数功能一样：`new(T)` 分配了零值填充的 `T` 类型的内存空间，并且 __返回其地址__，即一个 `*T` 类型的值。用 Go 的术语说，它返回了一个指针，指向新分配的类型 `T` 的零值。

`make` 只能创建 `slice`、`map` 和 `channel`，并且返回一个有初始值(非零)的 `T` 类型，而不是 `*T`

```go
p := new(int)  // p, of type *int, points to an unnamed int variable
fmt.Println(*p) // "0"
```

Each call to `new` returns a distinct variable with a unique address. There is one exception to this rule: two variables whose type carries no information and is therefore of size zero, such as `struct{}` or `[0]int`, may, depending on the implementation, have the same address.


## 多重赋值

```go
# tuple assignment
i, j = j, i
v, ok = m[key]  // map lookup
v, ok = x.(T)  // type assertion
v, ok = <-ch  // channel receive

// assign unwanted values to the blank identifier
_, err = io.Copy(dst, src)  // discard byte count
_, ok = x.(T)
```

可赋值性： the assignment is legal only if the __value__ is assignable to the type of the __variable__.

## 类型声明

A `type` declaration defines a new named type that has the same underlying type as an existing type:

```go
type name underlying-type_
```

A conversion from one type to another is allowed if both have the same underlying type, or if both are unnamed pointer types that point to variables of the same underlying type.

two values ofdifferent named types cannot be compared directly.

## packages and files

Each package serves as a separate name space for its declarations.

One package is initialized at a time, in the order of imports in the program, dependencies first. Initialization proceeds from the bottom up; the __main__ package is the last to be initialized.

## scope

The scope of a declaration is a region of the program text; it is a compile-time property.

The lifetime of a variable is the range of time during execution when the variable can be referred to by other parts of the program; it is a run-time property.

A name declared inside a syntactic block (lexical blocks) is not visible outside that block.

__universe block__ is a lexical block for the entire source code:

- built-in types
- built-in functions
- built-in constants

A program may contain multiple declarations of the same name so long as each declaration is in a different lexical block.

## 小结

Go 语言支持的基础类型：

- 布尔类型，bool
- 整型， int8, byte, int16, int, uint, uintptr 等
- 浮点类型， float32, float64
- 复数类型， complex64, complex128
- 字符串， string
- 字符类型， rune
- 错误类型， error

Go 语言支持的复合类型：

- 指针， pointer
- 数组， array
- 切片， slice
- 字典， map
- 通道， chan
- 结构体， struct
- 接口， interface
