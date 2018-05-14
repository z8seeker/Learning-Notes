# python 数据模型


## 1. 对象，值和类型

对象是 python 对数据的抽象。

All data in a Python program is represented by __objects__ or by __relations between objects__.

Every object has an identity, a type and a value:
- an object's identity never changes once it has been created. 
  - identity 可以认为是对象的内存地址
  - `is` 比较两个对象的 identity, 
  - `id()` 返回一个整数，表示对象的 identity
- an object's type determines the operations that the object supports and also defines the possible values for objects of that type. 
  - `type()`，返回对象的类型
  - an object's type is also unchangeable. 
- the value of some objects can change. 
  - mutable or immutable，当对象被创建后其值不可改变则为 immutable，否则为 mutable
  - An object's mutability is determined by its type. 

python 中的对象不会被显式的销毁，但当对象不可获得时（unreachable）会被垃圾回收：

- CPython uses a _reference-counting_ scheme with (optional) delayed detection of _cyclically linked garbage_
  - 这意味着 python 可以立刻回收不再被引用的对象（引用计数为零）
  - 而对有循环依赖的垃圾，则不一定会保证立刻回收，可以参考 gc 模块
- the use of the implementation's tracing or debugging facilities may keep objects alive that would normally be collectable
- catching an exception with a `try...except` statement may keep objects alive

某些对象可能包含对外部资源的引用，例如打开的文件或窗口等，当这些对象被垃圾回收时会释放这些资源，但因为不一定确保会发生垃圾回收，所以这些对象应该提供显式的方法（`close()`） 释放外部资源。这可以结合 `try...finally` 和 `with` 语句方便的实现。

某些对象会包含对其他对象的引用，因此也叫做容器， container，比如： tuples，lists 和 dict。当我们讨论容器的值时，我们是对针对容器说包含的对象的值而言的；而当我们讨论容器是否可变时（mutability），我们是针对容器所包含的对象的 identity 而言的。所以如果一个 tuple 包含一个对可变对象的引用，那这个 tuple 的值是会改变的，只要那个相应的可变对象改变。

Types affect almost all aspects of object behavior. Even the importance of object identity is affected in some sense: for immutable types, operations that compute new values may actually return a reference to any existing object with the same type and value, while for mutable objects this is not allowed.

```python
a = 1
b = 1
a is b // True

c = []
d = []
c is d // False
```

## 2. The standard type hierarchy

python 有以下内建类型：

### 2.1 None
This type has _a single value_. There is _a single object_ with this value.

It is accessed through the built-in name `None` and used to signify the absence of a value in many situations，比如当函数没有显式的返回任何值时将返回 None。

None 的真值为 false。

### 2.2 NotImplemented

This type has _a single value_. There is _a single object_ with this value.

It is accessed through the built-in name `NotImplemented`. Numeric methods and rich comparison methods should return this value if they do not implement the operation for the operands provided.

NotImplemented 的真值为 true。

### 2.3 Ellipsis

This type has _a single value_. There is _a single object_ with this value. 

This object is accessed through the literal `...` or the built-in name `Ellipsis`.

Ellipsis 的真值为 true。

### 2.4 numbers.Number

数值类型由数值字面量创建，数值类型对象是不可变对象。python 中的数值类型又可分为：

- numbers.Integral
- numbers.Real (float)
- numbers.Complex (complex)

#### 2.4.1 numbers.Integral

这种类型表示数学中的整数值（正整数和负整数），整数又可分为：

- Integers（int）
  - 这种类型可以表示无限大的范围（只要有足够的内存）
- Booleans (bool)
  - 这种类型表示真值：False 和 True
  - Boolean 类型对象只有两个对象，分别用于表示 False 和 True
  - Boolean 类型是整数类型的子类型
  - 几乎所有情况下，布尔值的行为分别与整数值 0 和 1 类似，唯一的例外是当布尔值被转换为字符串时，将会返回 "False" 或 "True"

#### 2.4.2 numbers.Real (float)

这种类型表示机器级（machine-level）的双精度浮点数。Python 不支持单精度的浮点数。

#### 2.4.3 numbers.Complex

这种类型使用一对双精度浮点数来表示一个复数。一个复数 `z` 的实部和虚部可以通过复数对象的只读属性 `z.real` `z.imag` 得到。

### 2.5 Sequences

序列类型表示有序的有限集合，并由非负整数进行索引。内建的 `len()` 函数返回序列的长度。当序列的长度为 n 时，这个序列的索引集合包括 `0, 1, ..., n-1`，序列的第 i 个元素可由 `a[i]` 得到。

序列类型也支持切片操作：`a[i:j]` 。当切片作为表达式使用时，一个切片的结果是一个同类型的序列

一些序列类型也支持扩展的切片操作： `a[i:j:k]`，第三个参数表示步长，会选择序列中所有满足这样条件的元素 `x`：`x = i + n*k, n>=0 and i<= x < j`

以值是否可变为依据，序列类型又可分为：

- immutable sequences
- mutable sequences

#### 2.5.1 Immutable sequences

- Strings
- Tuples
- Bytes

Strings

A string is a sequence of values that represent Unicode code points. 所有范围在 `U+0000 - U+10FFFF` 内的码点都可以在字符串中表示。

Python 没有字符类型，内建函数：
- `ord()` 将一个码点从字符串形式转换为一个范围在 `0 - 10FFFF` 之间的整数值；
- `char()` 将一个范围在 `0 - 10FFFF` 之间的整数值转换为相应的长度为 1 的字符串对象

str 与 bytes 之间的转换：

- `str.encode()`，使用特定编码，将一个 str 对象转换为一个 bytes 对象
- `btyes.decode()`，可以用来完成相反的操作，将一个 bytes 对象转换为一个 str 对象

Tuples

任何 python 对象都可以作为元组的元素。可以通过在一个表达式后面加逗号形成只有一个元素的元组。一个空元组可以用一对空的小括号表示。

Bytes

字节对象是一个不可变的数组，数组的元素是 8-bit 的字节（由 0 到 255 之间的整数表示）。字节字面量 （b'abc'）和内建函数 `bytes()` 可以创建 字节对象。通过使用 `decode()` 方法，字节对象可以被解码为字符串。


#### 2.5.2 Mutable sequences

- Lists
- Byte Arrays

对于可变序列类型对象，the _subscription and slicing_ notations can be used as the target of assignment and del (delete) statements.

Lists

列表的元素可以是任意 python 对象。

Byte Arrays

一个 bytearray 对象是一个可变的数组，由内建函数 `bytearray()` 进行创建。除了是可变的（因此也是不可hash 的），字节数组与不可变的字节对象有相同的接口和功能。

此外，标准库里 collections 模块还提供了一种可变的序列类型： `array`


### 2.6 Set types

集合类型表示 unordered, finite sets of unique, immutable objects. 因此，集合类型不能被索引。集合类型对象可以被迭代，内建函数 `len()` 返回集中中的元素个数。集合常见的使用场景包括：

- fast membership testing
- removing duplicates from a sequence
- computing mathematical operation，such as intersection，union， difference，and symmetric difference

对于集合元素，the same immutability rules apply as for dictionary keys。需要注意的是，数值类型遵循一般的数值比较规则：如果两个数相等（1 与 1.0），则只有一个数允许存在集合中。

目前，python 固有两种集合类型：

- Sets，可变的集合类型，由内建函数 `set()` 创建，创建后可以进行修改
- Frozen Sets，不可变的集合类型，由内建函数 `frozenset()` 创建，可以作为其他集合对象的元素或作为字典的键


### 2.7 Mappings

映射类型表示 finite sets of objects indexed by arbitrary index sets


### 2.8 Callable types

### 2.9 Modules

### 2.10 Custom classes

### 2.11 Class instances

### 2.12 I/O objects (file objects)

### 2.13 Internal types


## 3. Special method names

### 3.1 Basic customization

### 3.2 Customizing attribute access

### 3.3 Customizing class creation

### 3.4 Customizing instance and subclass checks

### 3.5 Emulating callable objects

### 3.6 Emulating container types

### 3.7 Emulating numeric types

### 3.8 With Statement Context Managers

### 3.9 Special method lookup


## 4. Coroutines

### 4.1 Awaitable Objects

### 4.2 Coroutine Objects

### 4.3 Asynchronous Iterators

### 4.4 Asynchronous Context Managers

