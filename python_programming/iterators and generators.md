## iterators & generators

### 一句话总结

迭代器是这样的对象：实现了无参数的 `__next__` 方法，返回序列中的下一个元素；如果没有元素了，就抛出 `StopIteration` 异常；还实现了 `__iter__` 方法，返回自身，因此也可以在使用可迭代对象的地方使用迭代器。调用生成器函数或使用生成器表达式时，会返回一个生成器对象，这个对象属于 python 语言内部的 `GeneratorType` 类型。因为 `GeneratorType` 类型的实例实现了迭代器协议, 所以所有的生成器都是迭代器。使用生成器可以实现惰性求值，节约内存占用。生成器还可以作为协程使用。


### 展开论述

#### 迭代器

迭代器用于遍历集合, 从中产出元素。迭代器不能/不应修改从数据源中读取的值, 只能/只应原封不动地产出值。python 在对对象进行迭代操作时的执行流程：

解释器需要迭代对象 x 时，会自动调用 `iter(x)`。内置的 `iter` 函数有以下作用：

1. 检查对象是否实现了 `__iter__` 方法，如果实现了就调用它，获取一个迭代器。
2. 如果对象没有实现 `__iter__()` 方法，但是实现了 `__getitem__（）` 方法，Python 会创建一个迭代器，尝试按顺序（从索引 0 开始）获取元素
3. 如果尝试失败，python 抛出 `TypeError` 异常，通常会提示“X object is not iterable”，其中 X 是目标对象所属的类。

可以看到在迭代过程中，其实是迭代器在发挥作用，因为迭代的第一步就需要把 __可迭代对象__ 转换为 __迭代器__。那首先什么是可迭代对象呢：
- 如果对象实现了能返回迭代器的 `__iter___` 方法，那么对象就是可迭代的
- 序列类型都是可以迭代的
- 实现了 `__getitem__` 方法，而且其参数是从零开始的索引，那么这种对象也是可以迭代的

Python 从可迭代的对象中获取迭代器。但可迭代的对象并不直接是迭代器，这是因为可迭代对象虽然需要实现 `__iter__` 方法，以便每次都实例化一个新的迭代器，但是可迭代对象却不用实现 `__next__` 方法。下面的代码可以清楚的看到这一点：

```python
# iterator
class MyIterator:
    def __init__(self, step):
        self.step = step

    def __next__(self):
        """return the next element"""
        if self.step == 0:
            raise StopIteration
        else:
            self.step -= 1
            return self.step

    def __iter__(self):
        """return the iterator itself"""
        return self


# iterable
class MyIterable:
    def __init__(self, number):
        self.step = number

    def __iter__(self):
        return MyIterator(self.step)


if __name__ == '__main__':
    mi = MyIterable(12)
    for i in mi:
        print(i)

```
#### 生成器
调用生成器函数或使用生成器表达式时，就会返回一个生成器对象。

生成器表达式，类似与列表推导，但使用的是圆括号而不是方括号。生成器表达式可以理解为列表推导式的惰性版本：不会迫切的构建列表，而是返回一个生成器，按需惰性生成元素。

```python
[expr for iter_var in iterable if cond_var]  # list comprehension
(expr for iter_var in iterable if cond_expr)  # generator expression
sum(i*i for i in range(10) if i%2)  # 165, parentheses omitted
```

只要 python 函数的定义体中有 `yield` 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象。生成器函数相当于是生成器工厂。

调用生成器函数返回的生成器对象,包装了生成器函数的定义体。当把生成器传给 `next(...)` 函数时, 生成器函数会向前,执行到函数定义体中的下一个 `yield` 语句, 返回产出的值, 并在函数定义体的当前位置暂停。最终, 当函数的定义体返回时, 外层的生成器对象会抛出 `StopIteration` 异常，这一点与迭代器协议一致。

生成器表达式是语法糖：完全可以替换成生成器函数，不过有时使用生成器表达式更便利。但是，生成器函数灵活得多, 可以使用多个语句实现复杂的逻辑, 也可以作为协程使用。此外，生成器函数有名称，因此可以重用。


#### 作为协程使用的生成器

python 2.2 引入了 `yield` 关键字，在 python 函数中使用 `yield` 语句就实现了生成器函数。python 2.5 将 `yield` 也可作为一个表达式使用，并为生成器对象添加了额外的方法和功能。当生成器函数被调用时，将返回一个生成器，这一生成器将控制生成器函数的执行过程：

1) 当生成器的方法被调用时，生成器函数才开始执行并一直执行到第一条 `yield expression`，在这里执行暂停(所有的局部状态将被保留)，并向生成器的调用方返回 `expression_list(containing at least one comma yields a tuple.)` 的值;

2) 通过继续调用生成器的某一方法 M， 生成器函数将从原来的状态继续执行，而此时 `yield expression` 的值视生成器被调用的方法 M 而定： 如果 M 为 `__next__()` 方法，则`yield expression` 的结果为 None;如果 M 为 `send(msg)`，则结果为 msg 的值。

生成器的各方法比较：

1) `send(msg) & __next__()`

`.send(msg)` 可以恢复并把值 msg 传递给生成器函数，而该 msg 将成为生成器函数中当前 `yield expression` 的返回值。而生成器函数中下一个由 `yield` 产生的值将被作为 `.send(msg)` 方法的返回值，若该生成器函数不再 `yield` 出值，`send(msg)`方法将返回（抛出）`StopIteration`异常。

而 `__next__()` 不能传递特定的值，只能传递 None 给生成器函数，调用该方法可启动或恢复生成器函数的执行，直到遇到下一个 `yield` 表达式，此时将该 `yield` 表达式 `<expression_list>` 的值返回给 `__next__()` 方法的调用方。该方法一般被隐式的调用（e.g. by a for loop）

第一次调用生成器时，应使用 `next()` 语句或是 `send(None)` 激活生成器，不能使用 `send` 发送一个非 None 的值，否则会出错，因为此时还没有 `yield expression` 来接收这个值。

2) `throw(type[, value[, traceback]])`

在生成器函数的当前 `yield expression` 处抛出（返回）类型为 type 的异常，异常值为 value，若该异常被捕获并处理，生成器函数中下一个 `yield expression` 将作为返回值给 `throw()`的调用方。如果生成器函数未能捕获该异常或产生了另一不同的异常，此时异常将传递回 `throw()` 方法的调用方。

3) `close()`
在生成器函数的当前 `yield expression` 处抛出（返回）类型为 `GeneratorExit` 的异常。如果此时的生成器函数优雅的推出，或已经关闭，或抛出 `GeneratorExit` 时，调用方不会报错，如果生成器收到 `GeneratorExit` 异常后有产出值，解释器将抛出 `RuntimeError` 异常。如果生成器抛出了其他的异常，此时异常将传递回 `close()` 的调用者。此外，当一个生成器对象被垃圾回收时将自动调用该方法。

在一个生成器函数中，如果没有 `return`，则默认执行至函数完毕，如果在执行过程中 `return`，则直接抛出 `StopIteration` 终止迭代。

在以上生成器方法中最值得关注的是 `.send(...)` 方法。与 `.__next__()` 方法一样, `.send(...)` 方法致使生成器前进到下一个 `yield` 语句。不过, `.send(...)` 方法还允许生成器的调用方把数据发给生成器函数, 不管传给 `.send(...)` 方法什么参数, 那个参数都会成为生成器函数定义体中对应的 `yield expression` 的值。也就是说, `.send(...)` 方法允许在 _调用方和生成器之间双向交换数据_。而  `.__next__()` 方法只允许调用方 _从生成器中获取数据_。这是一项重要的“改进”, 像这样使用的话, _生成器就变身为协程_。

但生成器与协程是不同的两个概念，不能混为一谈：
- 生成器用于生成 _供迭代的数据_
- 而协程是 _数据的消费者_
- 协程与迭代无关, 虽然在协程中会使用 `yield expression` 产出值，但这与迭代无关

PEP 380 中引入了一个新句法 `yield from`。`yield from` 允许生成器或协程把工作委托给第三方完成。此外，`yield from` 还会创建通道，把内层生成器直接与外层生成器的调用方联系起来。把生成器当成协程使用时, 这个通道特别重要, 因为这不仅使内层生成器能为调用方生成值, 还能让内层生成器使用调用方提供的值。



#### iter 函数释疑

标准库对 `iter` 函数的介绍：

- iter（object[, sentinel]) 函数

  Python标准库中对`iter`函数的描述
  return an iterator object.
  
  Without a second argument, object must be a __collection object__ which supports the iteration protocol (the` __iter__()` method), or it must support the sequence protocol (the` __getitem__()` method with integer arguments starting at 0). If it does not support either of those protocols, TypeError is raised.
  
  If the second argument, __sentinel__, is given, then object must be a __callable object__. The iterator created in this case will call object with no arguments for each call to its` __next__() `method; if the value returned is equal to sentinel, `StopIteration` will be raised, otherwise the value will be returned.
  
  One useful application of the second form of `iter() `is to read lines of a file until a certain line is reached. The following example reads a file until the` readline()` method returns an empty string:
```
  with open("mydata.txt") as fp:
      for line in iter(fp.readline, ''):
          process_line(line)
```
在涉及I/O处理的程序中，常常需要编写这样的代码：

```
CHUNKSIZE = 8192
def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data = b'':
            break
        process_data(data)
```
这样的代码可以用iter()函数替换如下：

```
def reader(s):
    for data in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)

```

