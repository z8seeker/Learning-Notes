
列表切片

对列表进行切片操作时，即使 start 或 end 索引越界也不会报错，利用这一特性，我们可以限定输入序列的最大长度：

```python
first_twenty_items = a[:20]
last_twenty_items = a[-20:]
```

注意：

当使用负变量作为 start 索引来切割变量时，如： `some_list[-n:]` 当 n 为 0 时，这个表达式则变成了原列表的一个浅拷贝

对原列表进行切片之后，会产生一个新列表（相当于深拷贝）

```python
a = [1, 2]
b = a
a[:] = [3, 4]
assert a is b  # true

b = a[:]
assert b == a and b is not a  # true
```


列表的步进式切割

```python
somelist[start:end:stride]
```

A common Python trick for reversing a byte string is to slice the string with a stride of -1:

```python
x = b'mongoose'
y = x[::-1]  # b'esoognom'
```

这种操作对已经编码成 UTF-8 字节串的 Unicode 字符则无法奏效。

不应该同时使用 `start, end, stride` 这三个参数进行列表切割操作。可以先做步进切割，再做范围切割：

```python
a = [i for i in range(10)]
b = a[::2]
c = b[1:-1]  # [1, 0]
```

或者使用 itertools 模块中的 `islice` 方法。


列表推导

列表推导比内置的 map 和 filter 函数更清晰。列表推导也支持多重循环：

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8,9]]
flat = [x for row in matrix for x in row]

squared = [[x**2 for x in row] for row in matrix]
```

列表推导处理的数据量过大时会占用大量内存，这时可以使用生成器表达式来进行改写：

```python
it = (len(x) for x in open('/tmp/my_file.txt'))
roots = ((x, x**0.5) for x in it)
```
串在一起的生成器表达式执行速度很快。


使用 enmuerate 获取序列类型或迭代器的值和位置信息：

```python
flavor_list = ['pecan', 'chocolate', 'strawberry']
for i flavor in enumerate(flavor_list, 1):
    print('%d: %s' %(i, flavor))
```

不要在循环后面使用 else 块，这种写法既不直观又容易引人误解。

`try/except/else/finally`

```python
# try/finally 既可将异常向上传播，又在异常发生时执行清理工作
try:
    pass
finally:
    pass

# try/except/else 哪些异常由自己的代码处理，哪些异常会传播到上级
def load_json_key(data, key):
    try:
        result_dict = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
    return result_dict[key]

```