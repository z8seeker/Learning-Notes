"""
Stack ADT implemented by a python list
"""
class ArrayStack:
    """
    a stack is a LIFO linear data structure.
    """
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        assert  not self.empty(), 'The stack is empty'
        return self._stack.pop()

    def peek(self):
        assert  not self.empty(), 'The stack is empty'
        return self._stack[-1]

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self._stack)


class Node:
    def __init__(value=None):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.root = Node()
    
    def add(self, node):
        node.next = self.root.next
        self.root.next = node
    
    def remove(self):
        if not self.root.next:
            return
        self.root.next.next = self.root.next
    
    def head(self):
        return self.root.next
    
    def empty(self):
        return self.root.next is None


class LinkedStack:

    def __init__(self):
        self._stack = LinkedList()
    
    def push(self, value):
        node = Node(value)
        self._stack.add(node)
    
    def pop(self):
        if not self.empty():
            node = self._stack.head()
            self._stack.remove()
            return node.value
    
    def peek(self):
        if not self.empty():
            node = self._stack.head()
            return node.value
    
    def empty():
        return self._stack.empty()
