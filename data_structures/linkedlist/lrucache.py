# lru cache using dict and doublely linkded list
# python3 内置标准库 functools.lru_cache
# 或借助与 collections.OrderedDict

import collections


class SimpleLRUCache(object):
    def __init__(self, size=8):
        self.size = size
        self.cache = collections.OrderedDict()
    
    def get(self, key):
        try:
            value = self.cache.pop(key)
        except KeyError:
            return
        else:
            self.cache[key] = value
            return value
    
    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.size:
                self.cache.popitem(last=False)
        self.cache[key] = value


class Node(object):
    def __init__(self, key=None, value=None):
        self.prev = self.next = None
        self.key, self.value = key, value


class CircularDoubleLinkedList(object):
    def __init__(self):
        node = Node()
        node.prev = node.next = node
        self.root = node
    
    @property
    def head(self):
        return self.root.next
    
    @property
    def tail(self):
        return self.root.prev
    
    def add(self, node):
        node.next = self.root
        node.prev = self.tail
        self.root.prev = self.tail.next = node
    
    def remove(self, node):
        if node is self.root:
            return
        node.prev.next = node.next
        node.next.prev = node.prev


class LRUCache(object):
    def __init__(self, size=8):
        self.size = size
        self.content = CircularDoubleLinkedList()
        self.cache = {}
    
    @property
    def full(self):
        return len(self.cache) >= self.size
    
    def __call__(self, func):
        def wrapper(*args):
            if args in self.cache:  # hit
                node = self.cache[args]
                self.content.remove(node)
                self.content.add(node)
            else:
                if self.full:
                    head = self.content.head
                    self.content.remove(head)
                    self.cache.pop(head.key)
                value = func(*args)
                node = Node(args, value)
                self.content.add(node)
                self.cache[args] = node
            return node.value
        return wrapper


@LRUCache(16)
def fib(n):
    if n == 0 or n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    value = fib(152)
    print(value)
