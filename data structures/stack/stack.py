"""
Stack ADT implemented by a python list
"""
class Stack:
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
