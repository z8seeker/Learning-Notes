# codecs - Codec registry and base classes

python 的 Standard Encodings:

`unicode_escape`, 产生一个 python unicode 字面量

```python
s = u'\\u0e4f\\u032f\\u0361\\u0e4f'
s.decode('unicode-escape')
```
