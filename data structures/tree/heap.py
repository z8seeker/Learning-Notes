# 堆的实现
# 堆的常用操作：往堆中插入一个元素，删除堆顶元素

import random


class Heap(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self._list = [None] * (self.capacity + 1)
        self.count = 0
    
    def insert(self, data):
        if self.count >= self.capacity:
            return
        else:
            self.count += 1
            self._list[self.count] = data
            self._shift_up()
    
    # 从下往上堆化
    def _shift_up(self):
        pos = self.count
        while (pos // 2 > 0 and self._list[pos] > self._list[pos // 2]):
            self._list[pos], self._list[pos // 2] = self._list[pos // 2], self._list[pos]
            pos = pos // 2
    
    def remove_max(self):
        if self.count == 0:
            return
        self._list[1] = self._list[self.count]
        self.count -= 1
        self._shift_down()
    
    # 从上往下堆化
    def _shift_down(self, pos=1):
        if pos * 2 <= self.count and self._list[pos] < self._list[pos * 2]:
            self._list[pos], self._list[pos * 2] = self._list[pos * 2], self._list[pos]
            self._shift_down(pos * 2)
        elif (pos * 2 + 1) <= self.count and self._list[pos] < self._list[pos * 2 + 1]:
            self._list[pos], self._list[pos * 2 + 1] = self._list[pos * 2 + 1], self._list[pos]
            self._shift_down(pos * 2 + 1)
        else:
            return


if __name__ == '__main__':
    a = list(range(10, 20))
    random.shuffle(a)
    print(a)
    h = Heap(10)
    for i in a:
        h.insert(i)
    print(h._list)
    h.remove_max()
    print(h._list)
