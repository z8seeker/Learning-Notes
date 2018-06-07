http 是无状态的协议，使用 session 可以让服务端知道当前的请求是哪个用户发出的。

一个 session 可以包含用户的多个信息。我们可以创建一个类用来表示 session。一个 session 需要有：

- 一个独一无二的 session id， 用来表示一个特定用户
- 存储表示用户信息的字段（键值对）
- 一个标志位，用来表示 session 在创建以后是否发生改变。当一个 session 实例进行了修改操作但没有被删除时，就说这个 session 是 dirty 的。

为了像使用字典一样方便的操作 session 表示的用户信息，我们可以定制 `__getitem__`, `__setitem__`, `__delitem__` 等魔术方法。同时为了正常的使用 `.` 进行属性操作，我们还需要实现 `__getattr__`, `__setattr__`, `__delattr__` 魔术方法。具体实现参考如下：

```python
class Session(object):
    def __init__(session_id, user_info_dict=None):
        self.session_id = session_id
        if user_info_dict:
            self.fields = dict(user_info_dict)
        else:
            self.fields = {}
        self._dirty = False
    
    def __getitem__(self, key):  # 实现 self[key]
        return self.fields[key]
    
    def __setitem__(self, key, value):  # 实现  self[key] = value
        self.fields[key] = value
        self._dirty = True

    
    def __delitem__(self, key):  # 实现 del self[key]
        del self.fields[key]
        self._dirty = True

    def __contains__(self, key):  # 实现 key in self
        return key in self.fields
    
    _DEFAULT_ARGUMENT = object() 

    def get(self, key, default=_DEFAULT_ARGUMENT):  # 实现类似字典的 get 方法
        if default is _DEFAULT_ARGUMENT:
            return self.fields[key]
        else:
            return self.fields.get(key, default)
    
    def __getattr__(self, key):  # 实现 self.key
        try:
            return self.fields[key]
        except KeyError:
            raise AttributeError
    
    def __setattr__(self, key, value):  # 实现 self.key = value
        if key in ('session_id', 'fields', '_dirty'):
            super(Session, self).__setattr__(key, value)
        else:
            self.fields[key] = value
            self._dirty = True
    
    def __delattr__(self, key):  # 实现 del self.key
        assert key not in ('session_id', 'fields', '_dirty')
        try:
            del self.fields[key]
        except KeyError:
            raise AttributeError
    
    @property
    def dirty(self):  # 实现 dirty 属性只读
        return self._dirty
    
    def __repr__(self):  # 友好显示
        return 'Session(session_id={0}, _dirty={1}) {2}\n'.format(self.session_id, self._dirty, self.fields)
```


上面主要讨论了 session 类应满足的功能和相应的实现。而一个 session manager 需要完成以下功能：

- 创建新的 session
- 将 session 保存到 redis 中
- 根据 session id 从 redis 中读取 session
- 根据 session id 从 redis 中删除 session
- 设置 session 过期时间


```python
from uuid import uuid4


class SessionManager(object):
    def __init__(self, redis):
        self.redis = redis
        self.expire_time = 3600 * 2
        self.key_prefix = 'session:'
    
    def new_session(self, session_id):
        if not session_id:
            session_id = uuid4().hex
        session = Session(session_id)
        session._dirty = True  # 表示需要进行保存
        return session
    
    def open_session(self, session_id):
        data = self.redis.get(self.key_prefix + session_id)
        if data:
            fields = json_decode(data)
            return Session(session_id, fields)
    
    def save_session(self, session):
        data = json_encode(session)
        self.redis.setex(
            self.key_prefix + session.session_id,
            self.expire_time,
            data
        )
        session._dirty = False
    
    def delete_session(self, token):
        self.redis.delete(self.key_prefix + token)
    
    def set_expire_time(self, expire_time):
        self.expire_time = expire_time
```
