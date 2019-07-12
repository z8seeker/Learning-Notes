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

### INTERFACES

