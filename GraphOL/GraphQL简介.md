# GraphQL

- [GraphQL 是什么？](#GraphQL-是什么)
- [GraphQL 的设计原则](#GraphQL-的设计原则)
- [为什么需要 GraphQL？(GraphQL 与 REST 的比较)](#为什么需要-GraphQL)
- [GraphQL 的 Python 实现](#GraphQL-的-Python-实现)
- [使用 GraphQL 的注意事项](#使用-GraphQL-的注意事项)
- [GraphQL 资源](#GraphQL-资源)

## GraphQL 是什么

GraphQL 是一个用于 API 的查询语言，是一个使用基于类型系统来执行查询的服务端运行时（类型系统由你的数据定义）。GraphQL 最初由 Facebook 在 2012 年开发，目的是为了解决移动应用的性能问题。Facebook 在 2015 年发布了 GraphQL 的 spec 和参考实现，现在 GraphQL 项目属于 GraphQL 基金会（托管于 Linux 基金会）。

一个 GraphQL 查询只会获取需要的数据，下面是一个简单的例子（https://graphql.org/swapi-graphql/）:

```code
# query
query {
    person(personID: 5) {
        name
        birthYear
        created
    }
}

# response, JSON data formatted to match the shape of the query
{
    "data": {
        "person": {
            "name": " Leia Orggna",
            "birthYear": "19BBY",
            "created": "2014-12-10T15:20:09.791000Z"
        }
    }
}
```

## GraphQL 的设计原则

GraphQL spec 里描述了 GraphQL 遵循以下设计原则：

- 分层（Hierarchical），GraphQL 的查询语句是嵌套（分层）的，与查询返回的数据形状相似
- 以产品为中心（Product centric）, GraphQL 是由客户端需要的数据驱动的
- 强类型 （strong typing），GraphQL Server 会定义一个应用层面的类型系统，所有的查询都会在这个类型系统的上下文中进行
- 客户端特定查询（Cilent-specified queries）， 通过类型系统，GraphQL Server 可以控制客户端获取哪些数据，同时客户端可以精确获取到需要的数据
- 自省（Introspective），一个 GraphQL Server 的类型系统可以通过查询语句进行查询


## 为什么需要 GraphQL

REST API 虽然简洁，每个 API 各司其职，但在实际使用中也会有以下问题：

1. 数据定制的问题。数据的返回可能很丰富，非常大，而我这次可能只要其中一小部分。虽然可以加个 Mask 参数解决，但是不够灵活。
2. 多次请求的问题。如果一次想多要些数据，往往我们就不得不使用多次的请求（为了渲染一个页面需要串行发起多个请求）。
3. 发出一个请求，不能确定会得到什么返回结果。你可能需要查阅文档，但文档可能已经过期。你可以自己实验，但你不知道是否覆盖了全部可能的情况。。。
4. 每个 resource 都有自己的一组 end point （URL），这会带来管理和维护的麻烦。
5. Rest 难以避免的从 URL 上接受各种参数（parameter），不严格的使用 GET 等都会造成安全的隐患。

REST 在现实世界里遇到的诸多问题使 GraphQL 应运而生。作为一个 API 的查询语言，GraphQL 从产品的角度出发，希望 API 足够灵活，能够处理复杂多变的用户场景。

相比于 REST API，使用 GraphQL 有以下优势：

1. GraphQL 对于异构的数据源能够很简练地处理。GraphQL 很适合作为一层薄薄的 API gateway，成为客户端和各种内部系统（包括 REST API）的一个桥梁。

2. GraphQL 的客户端可以很灵活地在服务器能力范围内进行各种查询的组合，这种能力对向后兼容和版本控制很有好处。对于同一 API，服务器只需要添加新的字段，新的客户端查询时使用新的字段即可，不会影响老客户端。

3. 对数据类型严格要求的 GraphQL 有助于减少类型不严格导致的问题。客户端可以放心大胆地根据事先给定的数据类型来使用服务端返回的结果，不必做许多额外的检查甚至是类型转换。

4. 良好的自说明性。使用 GraphQL 可以通过查询语句清晰、具体地描述这个请求的输入和输出。

使用 GraphQL 可以通过各种嵌套来达成你的查询目的，数据也不再是单一的资源，而形成了一个图，这是一种 _图形化的查询_。对于前端来说，你有什么样的 view, 需要什么样的数据，你就构建什么样的请求，得到的结果你就可以直接用来生成和填充你的 view。再复杂的 view 你也可以一次查询请求搞定，这对前端的反应速度和开发效率有很大的提升。

## GraphQL 的 Python 实现

使用 python 实现的用于构建 GrapQL server 的库有很多（详见：https://github.com/chentsulin/awesome-graphql#lib-py），比较成熟和使用广泛的是 Graphene 库。Graphene 和常用的 web 框架、ORM 都有集成：

- Flask-Graphql
- Graphene-Django
- Graphene-SQLAlchemy

Graphene 完全兼容于 GraphQL spec，可以和所有的 GraphQL 客户端（Realy, Apollo, gql等）无缝协作。

下面是一个使用 Graphene 的例子：

```python
import graphene


# build schema
class Query(graphene.ObjectType):
    hello = graphene.String(description="A typical hello world")

    def resolve_hello(self, info, name):
        return f"Hello, {name}!"

schema = graphene.Schema(query=Query)

# query
query = """
    query SayHello {
        hello(name: "World")
    }
"""
result = schema.execute(query)
print(result.data["hello"])  # Hello World!
```

相比于其他使用 _schema-first_ 方式实现的 GraphQL 库， Graphene 使用 _code-first_ 方式，用 python 代码来描述 GraphQL Server 的类型系统（而不是使用 Schema Definition Language, SDL）。

Schema 描述了 GraphQL Server 提供的数据模型的每个字段是什么类型。 Schema 还可以为字段定义各种参数（Arguments)。对于 Schema 中的每个字段（Field），我们需要写相应的 Resolver 方法，用于响应客户端查询。

## 使用 GraphQL 的注意事项

GraphQL 虽然有很多优点，但在实际使用中也有一些地方需要关注：

1. 使用 GraphQL 并不意味着能提高 API 效率，GraphQL 只定义了 API 的 UI 部分，是否比 REST API 高效取决于实现的方式。因为 GraphQL 每个 field 单独 resolve，很容易出现 N+1 query 问题。所以，在 resolve 的时候一定要合理地使用 dataloader。
2. GraphQL 的灵活性是把双刃剑。GraphQL 的查询能力隐含着很多安全上和性能上的问题，需要指定查询嵌套的上限，并且规定每个 API 的 timeout。
3. 使用 GraphQL 后旧有的缓存机制可能会失效。REST API 可以使用 nginx cache 或者 HA proxy 在 load balancer 级进行 API 的缓存 （如果 API 是幂等的）。但 GraphQL 的 query 都是以 POST 的方式提交，而 POST 并非幂等。
4. 使用 GraphQL 可能会增加实现的复杂度。原本的一些简单的 CRUD 的 API，在 GraphQL 下，会变得复杂起来。
5. 以往是根据 API（URL 端点）监控服务器性能和负载，使用 GraphQL 后一般只有一个入口，因此需要跟踪每个 resolver 行为的效率。

## GraphQL 资源

- Star Wars API. https://graphql.org/swapi-graphql/
- GraphQL Spec. https://graphql.github.io/graphql-spec/
- Github GraphQL API. https://developer.github.com/v4/
- awesome-graphql. https://github.com/chentsulin/awesome-graphql
- GraphQL engine. https://hasura.io
