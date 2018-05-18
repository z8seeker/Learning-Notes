# 创建型设计模式

创建型设计模式用来解决的问题是：在特定情景下，如何以最好的方式（灵活，可扩展）实例化一个对象。创建型设计模式包括：

- 单例模式，Singleton pattern
- borg 模式
- 工厂模式，Factory pattern
- 抽象工厂模式， Abstract Factory pattern
- 惰性加载模式， lazy_evaluation
- pool 模式
- 建造者模式，Builder pattern
- 原型模式，Prototype pattern


## 建造者模式

建造者模式是为了解决下面的问题：

- Encapsulate creating and assembling the parts of a complex object in a separate Builder object.
- A class delegates object creation to a Builder object instead of creating the objects directly.

A class (the same construction process) can delegate to _different Builder objects_ to create different representations of a complex object.

A builder is useful when you need to do lots of things to build an object. For example imagine a DOM. You have to create plenty of nodes and attributes to get your final object. 

简而言之，建造者模式的目的是为了解耦对复杂对象的创建和表示。

```python
# abstract building
class Building(object):

    def __init__(self):
        self.build_floor()
        self.build_size()
    
    def build_floor(self):
        raise NotImplementedError
    
    def build_size():
        raise NotImplementedError
    
    def __repr__(self):
        return f'Floor: {self.floor} | Size: {self.size}'


# concrete buildings
class House(Building):

    def build_floor(self):
        self.floor = 'one'
    
    def build_size(self):
        self.size = 'Big'

class Flat(Building):

    def build_floor(self):
        self.floor = 'More than One'
    
    def build_size(self):
        self.size = 'Small'
```


标准实现：

```python
"""
Separate the construction of a complex object from its representation so
that the same construction process can create different representations.
"""

import abc


class Director:
    """
    Construct an object using the Builder interface.
    """

    def __init__(self):
        self._builder = None

    def construct(self, builder):
        self._builder = builder
        self._builder._build_part_a()
        self._builder._build_part_b()
        self._builder._build_part_c()


class Builder(metaclass=abc.ABCMeta):
    """
    Specify an abstract interface for creating parts of a Product
    object.
    """

    def __init__(self):
        self.product = Product()

    @abc.abstractmethod
    def _build_part_a(self):
        pass

    @abc.abstractmethod
    def _build_part_b(self):
        pass

    @abc.abstractmethod
    def _build_part_c(self):
        pass


class ConcreteBuilder(Builder):
    """
    Construct and assemble parts of the product by implementing the
    Builder interface.
    Define and keep track of the representation it creates.
    Provide an interface for retrieving the product.
    """

    def _build_part_a(self):
        pass

    def _build_part_b(self):
        pass

    def _build_part_c(self):
        pass


class Product:
    """
    Represent the complex object under construction.
    """

    pass


def main():
    concrete_builder = ConcreteBuilder()
    director = Director()
    director.construct(concrete_builder)
    product = concrete_builder.product


if __name__ == "__main__":
    main()
```
