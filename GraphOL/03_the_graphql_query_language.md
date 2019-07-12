# The GraphQL Query Language

GraphQL takes the ideas that were originally developed to query databases and applies them to the internet. 

Compared with SQL:

- Instead of SELECT, GraphQL uses Query to request data
- Instead of INSERT, UPDATE,or DELETE, GraphQL wraps all of these data changes into one data type: the Mutation
- GraphQL includes a Subscription type that can be used to listen for data changes over socket connections

GraphQL query syntax is a string that looks the same regardless of whether the project uses JavaScript, Java, Haskell, or anything else. Queries are sent in the body of POST requests to a GraphQL endpoint:

```graphql
{
    allLifts {
        name
    }
}
```

```bash
curl  'http://snowtooth.herokuapp.com/'  -H 'Content-Type: application/json'  --data '{"query":"{ allLifts {name }}"}'
```

To modify data, we can send mutations. Mutations look a lot like queries, but their intention is to change something about the overall state of an application:

```
mutation {
    setLiftStatus(id: "panorama" status: OPEN) {
        name
        status
    }
}
```

```bash
curl 'http://snowtooth.herokuapp.com/'  -H 'Content-Type: application/json'  --data '{"query":"mutation {setLiftStatus(id: \"panorama\" status: OPEN) {name status}}"}'
```

## GraphQL API Tools

- GraphiQL
- GraphQL Playground

## Public GraphQL APIs

- https://developer.github.com/v4/explorer/
- https://graphql.org/swapi-graphql

## The GraphQL Query

```graphql
query {
    allLifts {
        name
        status
    }
}

# You can add multiple queries to a query document, 
# but you can run only one operation at a time
query {
    allLifts {
        name
        status
    }
}

query trails {
    allTrails {
        name
        difficulty
    }
}

query liftsAndTrails
```

With GraphQL, we are able to receive all kinds of different data points in a single query.

A Query is a _GraphQL type_. The fields that are available to query in a GraphQL API have been defined in that API’s schema.

The fields that we define in a selection set are directly realted to GraphQL types.

We can change the field names in the response object within the query by specifying an alias:

```graphql
query liftsAndTrails {
    open: liftCount(status: OPEN)
    chairlifts: allLifts {
        liftName: name
        status
    }
    skiSlopes: allTrails {
        name
        difficulty
    }
}

# a way to filter the results of a GraphQL query is to pass in query arguments.

# only the names of the closed chairlifts
query closedLifts {
    allLifts(status: "CLOSED" sortBy: "name") {
        name
        status
    }
}
# query the status of an individual chairlift by its unique identifier
query jazzCatStatus {
    Lift(id: "jazz-cat") {
        name
        status
        night
        elevationGain
    }
}
```

## Edges and Connections

In the GraphQL query language, fields can be either _scalar types_ or _object types_. 

Scalar types are the leaves of our selection sets. GraphQL comes with five built-in scalar types:

- Int
- Float
- String
- Boolean
- ID

GraphQL object types are groups of one or more fields that you define in your schema. We can connect objects together by querying one object for details about related objects.


## Fragments

Fragments are selection set that can be reused in multiple operations.

```graphql
# the fragment is name liftInfo, 
# and it is a selection set on the Lift type
fragment liftInfo on Lift {
    name
    status
    capacity
    night
    elevationGain
}

# using three dots with the fragment name
query {
    Lift(id: "jazz-cat") {
        ...liftInfo
        trailAccess {
            name
            difficulty
        }
    }
}
```

Fragments are selection sets on specific types, we must include the type that is associated with each fragment in its definition. 

We also can combine multiple fragments on the same type in a single selection set:

```graphql
query {
    allTrails {
        ...trailStatus
        ...trailDetails
    }

    fragment trailStatus on Trail {
        name
        status
    }

    fragment trailDetails on Trail {
        groomed
        trees
        night
    }
}
```

## UNION TYPES

```graphql
query schedule {
    agenda {
        # using inline fragments
        ...on work {
            name
            reps
        }
    ...on StudyGroup {
        name
        subject
        students
        }
    }
}

# using named fragments to query a union type
query today {
    agenda {
        ...workout
        ...study
    }
}

fragment workout on Workout {
    name
    reps
}
fragment study on StudyGroup {
    name
    subject
    students
}
```

## INTERFACES

An interface is an abstract type that establishes a list of fields that should be implemented in similar object types. When another type implements the interface, it includes all of the fields from the interface and usually some of its own fields.

When querying an interface, we can also use fragments to select additional fields when a specific object type is returned:

```graphql
query schedule {
    agenda {
        name
        start
        end
        ...on Workout {
            reps
        }
    }
}
```

Additionally request the `reps` when the ScheduleItem is a Workout.

## Mutations

Queries describe all of the reads that happen in GraphQL. To write new data, we use mutations. The Mutation is a root object type. 

Delete something:

```graphql
mutation burnItDown {
    deleteAllData
}
```

Whether the data is actually deleted ishandled by the implementation of the API.

Create something:

```graphql
mutation createSong {
    addSong(title:"No Scrubs", numberOne: true, performerName:"TLC") {
        id
        title
        numberOne
    }
}

# return
{  
    "data": {    
        "addSong": {      
            "id": "5aca534f4bb1de07cb6d73ae",      
            "title": "No Scrubs",      
            "numberOne": true    
        }  
    }
}
```

If the mutation field returns an object, you will need to add a selection set after the mutation. In this case, after it’s completed, the mutation will return the Song type that contains details about the song that was just created.

Change existing data:

```graphql
mutation closeLift {
    setLiftStatus(id: "jazz-cat" status: CLOSED) {
        name
        status
    }
}
```

### Using Query Variables

In GraphQL, variable names are always preceded by a `$` character.

```graphql
mutation createSong($title:String! $numberOne:Int $by:String!) {  
    addSong(title:$title, numberOne:$numberOne, performerName:$by) {    
        id    
        title    
        numberOne  
    }
}
```

## Subscriptions

A subscription allows us to listen to the GraphQL API for real-time data changes. Just like the mutation and the query, a subscription is a root type. Writing the GraphQL query to listen for a subscription is also similar to how we would define other operations.

```graphql
subscription {  
    liftStatusChange {    
        name    
        capacity    
        status  
    }
}
```

When we run this subscription, we listen for lift status changes over a WebSocket. Unlike queries and mutations, subscriptions remain open. To stop listening for status changes, you need to unsubscribe from your subscription.

## Introspection

Introspection is the ability to query details about the current API’s schema.

Introspection gives the client the ability to find out how the current API schema works.

## Abstract Syntax Trees

The query document is a string. When we send a query to a GraphQL API,that string is _parsed into an abstract syntax tree and validated before the operation is run_. 

The steps in this process:

- lexical analysis
- parsed into an AST

A query is much easier to dynamically modify and validate as an AST.

A document contains at least one definition, but it can also contain a list of definitions. Definitions are only one of two types: 

1. OperationDefinition, can contain only one of three operation types: mutation, query, subscription. Each opeartion defination contains the OperationType and the SelectionSet.
2. FragmentDefinition

ASTs are an essential part of GraphQL. Every operation is parsed into an AST so that it can be validated and eventually executed.
