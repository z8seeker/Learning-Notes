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
- the use of the implementation's tracing or debugging facilities may keep objects alive that would normally be collectable
- catching an exception with a `try...except` statement may keep objects alive

某些对象可能包含对外部资源的引用，例如打开的文件或窗口等，当这些对象被垃圾回收时会释放这些资源，但因为不一定确保会发生垃圾回收，所以这些对象应该提供显式的方法（`close()`） 释放外部资源。这可以结合 `try...finally` 和 `with` 语句方便的实现。

某些对象会包含对其他对象的引用，因此也叫做容器， container，比如： tuples，lists 和 dict。当我们讨论容器的值时，我们是对被容器包含的对象的值而言的；而但我们讨论容器是否可变时（mutability），我们是对被容器包含的对象的 identity 而言的。所以如果一个 tuple 包含一个对可变对象的引用，那这个 tuple 的值是会改变的，只要那个相应的可变对象改变。

Types affect almost all aspects of object behavior. Even the importance of object identity is affected in some sense: for immutable types, operations that compute new values may actually return a reference to any existing object eith the same type and value, while for mutable objects this is not allowed.

```python
a = 1
b = 1
a is b // True

c = []
d = []
c is d // False
```

## 2. The standard type hierarchy
Below is a list of the types that are built into Python:

- None
This type has a single value. There is a single object with this value.

It is accessed through the built-in name `None` and used to signify the absence of a value in many situations.

- NotImplemented

This type has a single value. There is a single object with this value.

It is accessed through the built-in name `NotImplemented`. Numeric methods and rich comparison methods should return this value if they do not implement the operation for the operands provided.

- Ellipsis
This type has a single value. There is a single object with this value. 

This object is accessed through the literal `...` or the built-in name `Ellipsis`.

- numbers.Number
- Sequences
- Set types
- Mappings
- Callable types
- Modules
- Custom classes
- Class instances
- I/O objects (file objects)
- Internal types

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

