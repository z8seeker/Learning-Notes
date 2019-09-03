# 使用 python 开发 GraphQL 服务

使用 graphene 包开发 GraphQL 服务。

在开发过程中，为避免同一套数据反复定义多次，可以使用 Graphene-SQLAlchemy 减少重复工作：

1. 令 GraphQL 的对象类型继承自 `SQLAlchemyObjectType` ，并在类中定义 `Meta` 类指定相关的 SQLAlchemy 映射类作为模型。`SQLAlchemyObjectType` 的 Meta 类支持通过 `exclude_fields` 属性指定不向客户端开放的字段。

2. 保留数据库定义与 GraphQL 对象类型定义不完全相同的字段。

在定义数据表时，通过谨慎选择关系的加载方式，可以避免无谓的数据库查询。

在完成数据库定义和底部数据层的集成后，需要将 GraphQL Schema 接入一个服务让客户端可以访问。

处理带文件的请求：

解决方法之一是把上传文件独立到单独的 API。

监控的细分：

以往是根据 API 监控服务器性能和负载，现在整个 GraphQL 只有一个入口，需要跟踪每个 resolver 行为的效率。


## graphene 中的类型

### Schema

schema 定义了 GraphQL API 的类型系统，描述了客户端能够获取到的数据集合（对象，字段，关系等）。来自客户端的调用首先会被验证 query 是否合法，然后再执行这个 query。客户端可以通过自省（type introspection）获取 schema 的信息。


```python
my_schema = Schema(
    query=MyRootQuery.
    mutation=MyRootMutation,
    subscription=MyRootSubscription
)
```

Auto CamelCase field names

默认情况下，所有的字段和参数名（只要没有显式设置 `name`）都将从 `snake_case` 转换到 `camelCase`。
to disable this behavior, set the `auto_camelcase` to `False` upon schema instantiation:

```python
my_schema = Schema(
    query=MyRootQuery,
    auto_camelcase=False,
)
```

### Scalars

graphene 中所有的标量类型都接受以下参数，所有的都是可选的：

- name, 字符串，覆写字段的名称
- description, 字符串，在 GraphiQL browser 中显示该类型的描述信息
- required, 布尔值，若为 `True` 则该字段是必须的
- deprecation_reason, 字符串，为这个字段提供弃用原因
- default_value, 为这个字段提供一个默认值

graphene 定义了以下几种基本标量类型：

- `graphene.String`, 文本数据
- `graphene.Int`, 有符号的 32 位整数
- `graphene.Float`, 有符号的双精度分数值
- `graphene.Boolean`, 布尔值
- `graphene.ID`, 表示一个 unique identifier, 在 JSON 响应中是字符串，而在作为输入类型时既可以是字符串也可以是整数
- `graphene.types.datetime.Date`, 日期数值（iso8601）
- `graphene.types.datetime.DateTime`, DateTime 数值 (iso8601)
- `graphene.types.datetime.Time`, 时间数值（iso8601)
- `graphene.types.json.JSONString`, JSON 字符串


定制标量类型

使用标量类型（Mounting Scalars）

标量可以在 `ObjectType`, `Interface` 或者 `Mutation` 里作为字段使用:

```python
class Person(graphene.ObjectType):
    name = graphene.String()

# 或者
class Person(graphene.ObjectType):
    name = graphene.Field(graphene.String)

# 在一个字段中使用 Types 时，是作为参数存在的
graphene.Field(graphene.String, to=graphene.String())

# 或者
graphene.Field(graphene.String, to=graphene.Argument(graphene.String))
```

### Lists and Non-Null

在 graphene 中只能定义对象类型，标量类型和枚举类型。可以使用类型修饰符（type modifiers）来验证相应的字段值。

```python
import graphene

class Character(graphene.ObjectType):
    name = graphene.NonNull(graphene.String)

# 等价于
class Character(graphene.ObjectType):
    name = graphene.String(required=True)

# List
class Charachter(graphene.ObjectType):
    appears_in = graphene.List(graphene.String)

# NonNull Lists
class Character(graphene.ObjectType):
    appears_in = graphene.List(graphene.NonNull(graphene.String))

```

### ObjectType

graphene 中的 _ObjectType_ 用来定义字段之间的关系：

- 每一个 `ObjectType` 都继承自 `graphene.ObjectType`
- `ObjectType` 的每个属性都表示一个字段
- 每个字段都有一个 `resolver method` 用来获取数据

#### Resolvers

Resolver 是一个方法，用来响应查询，获取 Schema 中相应字段的数据。 Resolvers 是惰性执行的，如果查询里不包括某个字段，则相应的 resolver 方法就不会执行。

Resolver 方法接受以下参数：

- Parent Value Object (parent), for the value object use to resolve most fields
- GraphQL Execution Info (info), query 和 schema 的元信息，以及请求上下文
- GraphQL Arguments (**kwargs), 定义在字段上的参数，作为关键字参数传递给 resolver 函数

Parent Value Object (parent)，是 resolver 方法的第一个参数，它的值是父字段（parent field）的 resolver 方法的返回值，如果没有父字段，它的值就是 `root_value` (可配置的值，默认为 `None`)。

```python
import graphene

class Person(graphene.ObjectType):
    full_name = graphene.String()

    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"

class Query(graphene.ObjectType):
    me = graphene.Field(Person)

    def resolve_me(parent, info):
        # return an object that represents a Person
        return get_human(name="Luke Skywalker")

schema = Schema(query=Query)

query_string = "{me { fullName }}"
result = schema.execute(query_string)
assert result["data"]["me"] == {"fullName": "Luke Skywalker"}
```

```python
import graphene

class Query(graphene.ObjectType):
    human_by_name = Field(Human, name=String(required=True))

    def resolve_human_by_name(parent, info, name):
        return get_human(name=name)

"""
    query {
        humanByName(name: "Luke Skywalker") {
            firstName
            lastName
        }
    }
"""
```

#### Graphene Resolvers 的特性

- Implicit staticmethod
- Default Resolver

graphene 会把所有的 reslover 方法当作静态方法进行处理，因此 reslover 方法的第一个参数永远不会是 `self`， 而是 `Parent Value Object`。这样处理是因为在 GraphQL 中，当 resolve 查询时我们往往更关心对象的 parent value object 而不是这个对象自身的属性。

如果 `ObjectType` 的字段没有定义 resolver 方法， Graphene 会提供一个默认的 resolver，如果 Parent Value Object (parent) 是一个字典，resolver 会查找对应的 key，否则 resolver 会查找对应的属性。

### 设置默认的 GraphQL 参数

```python
import graphene

class Query(graphene.ObjectType):
    hello = String(required=True, name=graphene.String())

    def resolve_hello(parent, info, name):
        return name if name else "World"
    
    # set default by combining all keyword arguments into a dict
    def reslove_hello(parent, info, **kwargs):
        name = kwargs.get("name", "World")
        return f"Hello, {name}!"
    
    # or by setting a default value for the keyword argument
    def resolve_hello(parent, info, name="World"):
        return f"Hello, {name}!"

# or set a default value for an Argument in the GraphQL schema itself
class Query(graphene.ObjectType):
    hello = graphene.String(required=True, name=graphene.String(default_value="World"))

    def resolve_hello(parent, info, name):
        return f"Hello, {name}!"
```

#### 在类外面写 Resolvers

```python
import graphene

def resolve_full_name(person, info):
    return "{} {}".format(person.first_name, person.last_name)

class Person(graphene.ObjectType):
    first_name = String()
    last_name = String()
    full_name = String(resolver=resolver_full_name)
```

#### 配置 ObjectType - 元类

Graphene 使用 `Meta inner class` 对 `ObjectType` 作不同的设置:

- 类型名
- 类型描述
- 接口 （和 possible types）

```python
import graphene

Song = namedtuple("Song", ('title', 'artist'))

class MyGraphQLSong(ObjectType):
    ''' We can set the schema description for an Object Type here on a docstring '''
    class Meta:
        name = "Song"  # set type name to Song
        description = '''But if we set the description in Meta, this value is used instead'''  # set type description
        interface = (graphene.Node, )
        possible_types = (Song, )
```

### Enums

definition:

```python
import graphene

class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6

    # value descriptions
    @property
    def description(self):
        if self == Episode.NEWHOPE:
            return "NEW HOPE EPISODE"
        return "Other episode"

# or using instances of Enum
Episode = graphene.Enum("Episode", [("NEWHOPE", 4), ("EMPIRE", 5), ("JEDI", 6)])
```

Graphene 中的 `Enum` 类在内部使用标准库的 `enum.Enum` 实现，但在获取成员时稍有区别：

```python
from graphene import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

assert Color.get(1) == Color.RED
```
