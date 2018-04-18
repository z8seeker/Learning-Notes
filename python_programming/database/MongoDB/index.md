# MongoDB 中的索引简介

在 MongoDB 里，索引支持高效的查询操作，如果没有索引，MongoDB 必须对整个集合进行扫描，如果设置了合适的索引，可以有效的限制需要检查的文档数量。

索引是特殊的数据结构（B 树），索引可以存储一个特定字段或一组特定字段的值，然后根据字段的值进行排序。经过排序的索引可以支持高效的相等性匹配和范围匹配。

从根本上看，MongoDB 中的索引与其他数据库中的索引是类似的。MongoDB 在集合这个层级定义索引，支持将任意字段或子字段定义为索引。

## 默认的索引 `_id`

在创建集合时，MongoDB 会自动在 `_id` 字段创建一个 unique index， `_id` 字段上的这个索引是无法删除的。

## 创建索引

可以使用 `db.collection.createIndex()` 在 Mongo shell 里创建索引：

```javascript
db.collection.createIndex(<key and index type specification>, <options>)
```

`db.collection.createIndex` 方法只在将要创建的索引不存在时才会创建这个索引。

## 索引类型

MongoDB 提供了多种索引类型以支持特定类型的数据和查询。

### 单个字段索引（Single Field）

对一个文档中的某一个字段创建升序或降序索引：

```javascript
{score: 1}
```
对于单个字段索引，排序的顺序是无关紧要的，因为 MongoDB 可以从任意方向对索引进行遍历。

### 复合索引（compound Index）

对文档中的多个字段创建索引，这就是复合索引。

复合索引中的字段次序是有意义的：

```javascript
{suerid: 1, score: -1}
```
这个索引首先按照 userid 排序，然后对于每个 userid 再按照 score 排序。

对于复合索引和排序操作而言，索引键的排序次序可以决定这个索引能否支持排序操作。

### 多个键的索引（Multikey Index）

MongoDB 使用“多个键的索引”用来索引存储在数组中的内容。如果索引的字段对应的是数组，MongoDB 将为数组中的每个元素创建独立的索引。MongoDB 会自动决定是否创建多个键的索引，因此不需要显式的指定 索引的类型为 multikey type

### 空间位置索引（Geospatial Index）

为支持高效的查询空间坐标数据，MongoDB 提供了两种空间索引



## 常用的索引操作

### 查看集合中的已有索引

```javascript
db.people.getIndexes();
```

### 从集合中删除索引

从集合中删除索引有两种方法：

1. `db.collection.dropIndex()`
2. `db.collection.dropIndexes()`

#### 删除特定的一个索引

此时应使用 `db.collection.dropIndex()` 方法，这个方法返回的结果是一个文档，包含了这个操作的状态信息。

```javascript
db.account.dropIndex({'tax-id': 1}); // {"nIndexesWas": 3, "ok": 1}
```

`nIndexesWas` 表示在删除这个索引前，集合中的索引数目

#### 删除所有的索引

使用 `db.collection.dropIndexes()` 删除除了 `_id` 之外的所有索引

### 修改索引

需要修改一个索引时，需要先 `drop` 然后再 `recreate` 这个索引。

