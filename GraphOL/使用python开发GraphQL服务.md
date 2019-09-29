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

### Interfaces

接口是一种抽象类型，它包含了一组字段。为了实现这个接口，相应的类型也必须包含这些字段。

```python
import graphene

class Character(graphene.interface):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    friends = graphene.List(lambda: Character)


class Droid(graphene.ObjectType):
    class Meta:
        interfaces = (Character, )
    
    primary_function = graphene.String()

class Query(grphene.ObjectType):
    hero = graphene.Field(Character, required=True, epidsode=grapee=graphene.Int(required=True))

    def resolve_hero(root, info, episode):
        if episode = 5:
            return get_human(name='Luke skywalk')

schema = graphnene.Schema(query=Query, types=[Droid])
```

当需要返回不同类型的对象集合时。使用接口是很有用的。

#### Resolving data objects to types

在接口中定义 `resolve_type` 类方法，将数据对象映射为一个 Graphene 类型：

```python
import graphene
class Character(graphene.Interface):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)

    @classmethod
    def resolve_type(cls, instance, info):
        if instance.type == 'DROID':
            return Droid
        return Human
```


### Unions

每一个 Union 对象都是继承自 `graphene.Union` 的 python 类。Union 类型自身不含有任何字段，只是链接到相应的 object types。这些被链接到的 object types 必须是具体的类型，而不能是 interface 或 Union 类型。

```python
import graphene

class Human(graphene.ObjectType):
    name = graphene.String()
    born_in = graphene.string()

class Droid(graphene.ObjectType):
    name = graphene.String()
    primary_function = graphene.String()

class SearchResult(graphene.Union):
    class Meta:
        types = (Human, Droid, Starship)

```

### Mutations

Mutation 是一种特殊的 ObjectType，定义有 Input

```python
import graphene

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
    
    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, name):
        person = Person(name=name)
        ok = True
        return CreatePerson(person=person, ok=ok)

class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()

class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()

# We must define a query for our schema
class Query(graphene.ObjectType):
    person = graphene.Field(Person)

schema = graphene.Schema(query=Query, mutation=MyMutations)
```

#### InputFields 和 InputObjectTypes

定义 InuptObjectType 指定提交数据的结构，然后可以在 Mutation 类型中使用相应的 InputFields。InputObjectTypes 类型在定义时允许嵌套，方便构造复杂的输入数据（input data）：

```python
import graphene

class LatLngInput(graphene.InputObjectType):
    lat = graphene.Float()
    lng = graphene.Float()

class LocationInput(graphene.InputObjectType):
    name = graphene.String()
    latlng = graphene.InputField(LatLngInput)
```

#### Output type

如果要返回一个已存在的对象类型，而不需指定特定的 mutation 类型，可以直接设置 Output 属性：

```python
import graphene

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    Output = Person

    def mutate(root, info, name):
        return Person(name=name)
```

### AbstractTypes

AbstractType 中包含的字段可以在 ObjectType, Interface, InputObjectType, 或其他 AbstractType 中共享：

```python
import graphene

class UserFields(graphene.AbstractType):
    name = graphene.String()

class User(graphene.ObjectType, UserFields):
    pass

class UserInput(graphene.InputObjectType, UserFields):
    pass
```

## graphene 查询的执行过程

执行一个查询时，可直接调用 Schema 的 execute 方法：

```python
from graphene import Schema

schema = Schema(...)
result = schema.execute('{ name }')
```

`result.data` 是查询的执行结果，`result.errors` 保存的是错误信息（None 或 非空 list）

### Context（上下文）

可以通过 context 参数向查询传递上下文信息：

```python
import graphene

class Query(graphene.ObjectType):
    name = graphene.String()

    def resolve_name(root, info):
        return info.context.get('name')

schema = Schema(Query)
result = Schema.execute('{ name }', context={'name': 'Syrus'})
```

### Variables

通过 variables 参数向查询传递变量信息：

```python
result = Schema.execute('...', variables={'id': 12})
```

### Root Value

通过 root 参数可以覆写 root queries 和 mutations 中的 Parent Value Object。

### Operation Name

如果一个查询中包含多个查询操作，可以指定 `operation_name` 来指明需要执行哪个操作。

