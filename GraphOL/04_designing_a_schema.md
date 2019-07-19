# Designing a Schema

Before breaking ground on your new API, you need to formally define the data types that your API will expose. This collection of types is called a schema.


The Schema Definition Language, or SDL is the same no matter what language or framework you use to construct your applications. They are later used by both clients and servers to validate GraphQL requests.

At the heart of all GraphQL projects is a solid, well-defined schema.This serves as a roadmap and a contract between the frontend and backend teams to ensure that the product built always serves the schema.

## Defining Types

The core unit of any GraphQL Schema is the type. A type represents a custom object and these objects describe your application's core features.

A type has fields that represent the data associated with each object. Each field returns a specific type of data.

You can write your schema in any text file, which usually carries the `.graphql` extension.

GraphQL's built-in types are called scalar types:

- String, will be JSON string
- ID, used when a unique identifier should be returned, will be JSON string
- Boolean
- Int
- Float

###  Define your own custom scalar types

A scalar type is not an object type. It doesn't have fields.

### Enums

Enums are scalar types:

```graphql
enum PhotoCategory {
    SELFIE
    PORTRAIT
    ACTION
    LANDSCAPE
    GRAPHIC
}
```

## Connections and Lists

Lists are created by surrounding a GraphQL type with square brackets. 

Most list definitions are non-nullable lists of non-nullable values. An empty array is technically not null: it is just an array that doesn’t contain any values.

One-to-One Connections:

```graphql
type User {    
    githubLogin: ID!    
    name: String    
    avatar: String
}

type Photo {    
    id: ID!    
    name: String!    
    url: String!    
    description: String    
    created: DateTime!    
    category: PhotoCategory!    
    postedBy: User!
}
```

### Use lists to connect object types

One-to-Many Connections

It is a good idea to keep GraphQL services undirected when possible. (flexibility) :

```graphql
type User {
    githubLogin: ID!
    name: String
    avatar: String
    postedPhotos: [Photo!]!
}
```

A common place to add one-to-many connections is in our root types.

```graphql
type Query {
    totalPhotos: Int!
    allPhotos: [Photo!]
    totalUsers: Int!
    allUsers: [User!]
}

schema {
    query: Query
}

# photos and users can be queried with the following query string
query {
    totalPhotos
    allPhotos {
        name
        url
    }
}
```

Many-to-Many Connections

```graphql
type User {
    ...
    inPhotos: [Photo!]
}

type Photo {
    ...
    taggedUsers: [User!]!
}
```

### THROUGH TYPES

A through type object is a node that is designed to connect two nodes:

```graphql
type User {
    friends: [Friendship!]!
}

type Friendship {
    friend_a: User!
    friend_b: User!
    howLong: Int!    
    whereWeMet: Location
}

# improved the design
type Friendship {
    friends: [User!]!
    how_long: Int!
    where_we_met: Location
}
```

## Lists of Different Types

In GraphQL, our lists do not always need to return the same type. (Union types and interfaces)

### UNION TYPES

In GraphQL, a union type is a type that we can use to return one of several different types:

```graphql
union AgendaItem = StudyGroup | Workouttype 

type StudyGroup {    
    name: String!    
    subject: String    
    students: [User!]!
}

type Workout {    
    name: String!    
    reps: Int!
}

type Query {    
    agenda: [AgendaItem!]!
}
```

If the objects contain completely different fields, it is a good idea to use union types.


### INTERFACES

Interfaces are abstract types that can be implemented by object types.

```graphql
scalar DateTime

interface AgendaItem {
    name: String!
    start: DateTime!
    end: DateTime!
}

type StudyGroup implements AgendaItem {
    name: String!
    start: DateTime!
    end: DateTime!
    participants: [User!]!
    topic: String!
}

type Workout implements AgendaItem {
    name: String!
    start: DateTime!
    end: DateTime!
    reps: Int!
}

# any type that implements the AgendaItem interface can be returned in the agenda list
type Query {
    agenda: [AgendaItem!]!
}
```

## Arguments

Arguments can be added to any field in GraphQL. They allow us to send data that can affect outcome of our GraphQL operations.

```graphql
type Query {
    ...
    User(githubLogin: ID!) User!
    Photo(id: ID!): Photo!
}
```

Just like a field, _an argument must have a type_. That type can be defined using any of the scalar types or object types that are available in our schema.

## Filtering Data

```grapql
type Query {
    ...
    allPhotos(category: PhotoGategory): [Photo!]!
}

query {
    allPhotos(category: "SELFIE") {
        name
        description
        url
    }
}
```

### Data Paging

We can use GraphQL arguments to control the amount of data that is returned from our queries.

To implement data paging, we are going to add _two optional arguments_:

1. `first` to collect the number of records that should be returned at once in a single data page, 
2. `start` to define the starting position or index of the first record to return. 

```graphql
type Query {
    ...
    allUsers(first: Int=50 start: Int=0): [User!]!
    allPhotos(first: Int=25 start: Int=0): [Photo!]!
}

# select usrs 90 through 100
query {
    allUsers(first: 10 start: 90) {
        name
        avatar
    }
}
```

### Sorting

We can _use arguments_ to define how the returned list of data should be sorted.

One way to tackle this challenge is to create _enums_ that specify which fields can be used to sort objects and instructions for how to sort those fields:

```graphql
enum SortDirection {
    ASCENDING
    DESCENDING
}

enum SortablePhotoField {
    name
    description
    category
    created
}

Query {
    allPhotos(
        sort: SortDirection = DESCENDING
        sortBy: SortablePhotoField = created
    ): [Photo!]!
}
```

## Mutations

Mutations also are defined in their own custom object type and added to the schema.

When designing your GraphQL service, make a list of all of the actions that a user can take with your application. Those are most likely your mutations.

```graphql
# post metadata about photo, not uploading
type Mutation {
    postPhoto(
        name: String!
        description: String
        category: PhotoCategory=PORTRAIT
    ): Photo!
}

schema {
    query: Query
    mutation: Mutation
}

mutation {
    postPhoto(name: "Sending the Palisades") {
        id
        url
        created
        postedBy {
            name
        }
    }
}
```

## Input Types

An input type is similar to the GraphQL object type except it is used for input arguments.

We can organize and reuse all of our sorting and filtering fields by using input types.

## Return Types

We can use custom return types on any field for which we need more than simple payload data. For example, when a user has signed in and been authenticated, we need to return a token in addition to the User payload:

```graphql
type AuthPayload {
    user: User!
    token: String!
}

type Mutation {
    ...
    githubAuth(code: String!): Authpayload!
}
```

## Subscriptions

 It will be up to us to make sure the subscriptions implement the PubSub design pattern along with some sort of real-time transport when we build the GraphQL service.

 ```graphql
type Subscription {
    newPhoto(category: PhotoCategory): Photo!
    newUser: User!
}

schema {
    query: Query
    mutation: Mutation
    subscription: Subscription
}
 ```

A subscription is a great solution when it’s important to handle data in real time.

## Schema Documentation

By adding three quotation marks above and below your comment on each type or field, you provide users with a dictionary for your API. In addition to types and fields, you can also document arguments.

At the heart of all GraphQL projects is a solid, well-defined schema. This serves as a roadmap and a contract between the frontend and backend teams to ensure that the product built always serves the schema.

