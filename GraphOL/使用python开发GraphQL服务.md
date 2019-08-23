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
