# GraphQL 入门

GraphQL 是一个用于 API 的查询语言，是一个使用基于类型系统来执行查询的服务端运行时（类型系统由你的数据定义）。

GraphQL consists of a type system, query language and execution semantics, static validation, and type introspection.

Major GraphQL clients include Apollo Client and Relay. GraphQL servers are available for multiple languages, including Haskell, JavaScript, Perl, Python, Ruby, Java, C#, Scala, Go, Elixir, Erlang, PHP, R, and Clojure.

On 9 February 2018, the GraphQL Schema Definition Language (SDL) was made part of the specification.

## 简单回顾

Getting data from a server to the client quickly and predictably is the story of the web, past, present, and future.

## 什么是 GarphQL

GraphQL is a query language for your APIs. It’s also a runtime for fulfilling queries with your data. 

The query of GraphQL is nested, and when it is executed, can traverse related objects. With GraphQL, our clients can obtain all of the data they need in one request.

Every GraphQL service defines types in a GraphQL schema. You can think of a type system as a blueprint for your API’s data, backed by a list of objects that you define. 

```graphql
# The Person type defines all of the fields, along with their types
type Person {
    id: ID!    
    name: String    
    birthYear: String    
    eyeColor: String    
    gender: String    
    hairColor: String    
    height: Int    
    mass: Float    
    skinColor: String    
    homeworld: Planet    
    species: Species    
    filmConnection: PersonFilmsConnection    
    starshipConnection: PersonStarshipConnection    
    vehicleConnection: PersonVehiclesConnection    
    created: String    
    edited: String
}
```

GraphQL is often referred to as a _declarative data-fetching_ language.

## The GraphQL Specification

GraphQL 是一个 client-server 通信的标准。

The spec describes the language and grammar you should use when writing queries. It also sets up a type system plus the execution and validation engines of that type system.


## Design Principles of GraphQL

- Hierarchical. Fields are nested within other fields and the query is shaped like the data that it returns.
- Product centric. GraphQL is driven by the data needs of the client and the language and runtime that support the client.
- Strong typing. Each data point has a specific type against which it will be validated.
- Client-specified queries. A GraphQL server provides the capabilities that the clients are allowed to consume.
- Introspective. The GraphQL language is able to query the GraphQL server's type system

## Origins of GraphQL

在 2012 年， Facebook 为了解决移动应用的性能问题，"rethink their data from the client side"，发明了 GraphQL。并在 2015 年发布了 GraphQL 的 spec 和参考实现

## History of Data Transport

When we think about data transport, we’re trying to make sense of how to pass data back and forth between computers. We request some data from a remote system and expecta response.

### Remote Procedure Call

1960 年代， RPC 被发明了出来。 The flow of information was basically the same with today's clients and servers： request some data from the client, get a response from the server.

### Simple Object Access Protocol

1990 年代末期，SOAP 出现了。SOAP used XML to encode a message and HTTP as a transport. 

SOAP implementations were fairly complicated.

### REST

REST 在 2000 年出现。

In a RESTful architecture, routes represent information。REST allows us to create a data model with a variety of endpoints, a far simpler approach than previous architectures.

### REST Drawbacks

- Overfetching, we’re getting a lot of data back that we don’t need.
- Underfetching, we're making additional requests for more data.

The GraphQL solution to underfetching is to _define a nested query_ and then request the data all in one fetch.

### Managing REST Endpoints

Another common complaint about REST APIs is the lack of flexibility. Development speed can be slow because setting up new endpoints often means that frontend and backend teams have more planning and communication to do with each other.

With GraphQL, the typical architecture involves a single endpoint.

Setting up a GraphQL endpoint that fetches data from REST endpoints is a perfectly valid way to use GraphQL. It can be a great way to incrementally adopt GraphQL at your organization.

### Github why user GraphQL

We heard from integrators that our REST API also wasn’t very flexible. It sometimes required two or three separate calls to assemble a complete view of a resource. It seemed like our responses simultaneously sent too much data and didn’t include data that consumers needed.

### GraphQL in the Real World

Github's REST API went through three iterations, and version 4 of its public API uses GraphQL: "the ability to define precisely the data you want-and only the data you want-is a powerful advantage over the REST API v3 endpoints"

### GraphQL Clients

GraphQL clients have emerged to speed the workflow for developer teams and improve the efficiency and performance of applications. They handle tasks like:

- network request
- data caching
- injecting data into the user interface

Relay is Facebook’s client that works with React and React Native.

Apollo Client supports all major frontend development platforms and is framework agnostic.

