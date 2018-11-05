# python 中表示字符序列的类型

python3

- bytes, 8位的二进制字节序列 
- str, Unicode 字符序列



python2

- str, 二进制字节
- unicode, Unicode 字符

## Unicode 字符转换为二进制数据

把 Unicode 字符表示为二进制数据，需要进行编码（encode），最常见的编码方式是 `UTF-8`

python3 的 str 实例和 python2 的 unicode 实例没有和特定的二进制编码形式相关联，必须使用 encode 方法才能转换为二进制数据。


## 二进制数据转换为 Unicode 字符

把二进制数据表示为 Unicode 字符，需要进行解码（decode）。


## 处理 python 中的编码问题

把编码和解码放在程序最外层处理，程序的核心部分使用 Unicode 字符类型，而不要对字符编码做任何假设。

python3 中 接收 str 或 bytes，并总是返回 str/bytes 的方法：

```python
def to_str(str_or_bytes):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode('UTF-8')
    else:
        return str_or_bytes


def to_bytes(str_or_bytes):
    if instance(str_or_bytes, str):
        return str_or_bytes.encode('UTF-8')
    else:
        return str_or_bytes
```

python2 中的处理方法与 python3 类似。


注意：

- 在 python3 中 bytes 实例和 str 实例之间不能使用操作符（>, +）
- 在 python2 中如果 str 实例只包含7位的二进制字符，则可以和 unicode 之间使用操作符
python3 中如果通过内置的 open 函数获取文件句柄，该句柄默认会采取 UTF-8 编码格式来操作文件（python2 中默认采取二进制形式）。这样在文件句柄上进行 read 和 write 操作时，必须传入包含 Unicode 字符的 str 实例，而不能是 bytes 实例。

同时适配 python2 与 python3:

```python
with open('/tmp/random.bin', 'wb') as f:
    f.write(os.urandom(10))
```

