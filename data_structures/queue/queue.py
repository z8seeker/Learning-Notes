# 使用数组和链表实现队列


class ArrayQueue:
    def __init__(self, size):
        self.size = size
        self._queue = list()
        self.head = self.tail = 0
    
    def empty(self):
        return self.head == self.tail
    
    def full(self):
        return self.size == self.tail and self.head == 0
    
    def enqueue(self, item):
        if self.full(): 
            return False
        else:
            if self.tail == self.size:
                # 队列未满，但 tail 已指向尾部，进行数据搬移
                for i in range(self.head, self.tail):
                    self._queue[i - self.head] = self._queue[i]
                self.tail -= self.head
                self.head = 0
        self._queue[self.tail] = item
        self.tail += 1
        return True
    
    def dequeue(self):
        if self.empty():
            return None
        item = self._queue[self.head]
        self.head += 1
        return item


class CircularQueue:
    def __init__(self, size):
        self.size = size
        self._queue = list()
        self.head = self.tail = 0
    
    def empty(self):
        return self.head == self.tail
    
    def full(self):
        return (self.tail + 1) % self.size == self.head
    
    def enqueue(self, item):
        if self.full():
            return False
        else:
            self._queue[self.tail] = item
            self.tail = (self.tail + 1) % self.size
            return True
    
    def dequeue(self):
        if self.emtpy():
            return None
        else:
            item = self._queue[self.head]
            self.head = (self.head + 1) % self.size
            return item


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
        node = self.root
        while node.next and node.next.next:
            node = node.next
        tail = node.next
        # remove tail
        node.next = None
        return tail

    def empty(self):
        return self.root.next is None


class LinkedQueue:
    def __init__(self):
        self._queue = LinkedList()
    
    def empty():
        return self._queue.empty()
    
    def enqueue(self, item):
        node = Node(item)
        self._queue.add(node)
    
    def dequeue(self):
        if self.empty():
            return None
        else:
            node = self._queue.remove()
            return node.value
