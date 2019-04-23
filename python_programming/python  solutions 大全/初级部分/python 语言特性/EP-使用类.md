# 类与继承

用来保存程序状态的数据结构一旦变得过于复杂（使用字典嵌套多于一层，或元组里的元素多于两项）时，就应该将其拆解为类，以便提供更为明确的接口，并更好的封装数据。

使用 namedtuple 定义出精简而又不可变的数据类：

```python
import collections

Grade = collections.namedtuple('Grade', ('score', 'weight'))
```

 Grade 的字段都可以通过属性名称访问。

 使用容器类。


 为类定义 `__call__` 方法， `__call__`

 属性的种类：

 - public
 - protected
 - private

 使用 property

- 定义访问对象属性时的行为
- 不应该在某属性的 getter 方法里修改其他属性的值
- 只在 `@property.setter` 方法里面修改相关的对象状态，而且要防止产生副作用
- 能够迅速返回，应该把执行开销比较大的操作放到普通的方法里


使用 weakref 模块的 `WeakKeyDictionary`，可以避免对象的引用计数无法降为 0


```python
class LazyDB(object):
    def __init__(self):
        self.exists = 5
    
    def __getattr__(self, name):
        value = 'Value for {}'.format(name)
        setattr(self, name, value)
        return value
```

上面这种模式适合实现无结构数据（schemaless data）的按需访问（惰性访问）


若需要在 `__getsttribute__` 和 `__setattr__` 方法中访问示例属性，应该直接通过 `super()` 进行操作，以避免无限递归。

