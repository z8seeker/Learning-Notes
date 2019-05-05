# 堆排序


def heap_sort(alist):
    # 首先建堆, 使用从上往下方式
    length = len(alist)
    for pos in range((length - 1) // 2, -1, -1):
        heapify(alist, length, pos)
    
    # 开始排序
    for pos in range(length - 1, 0, -1):
        # 将堆顶数据依次放置到最后
        alist[pos], alist[0] = alist[0], alist[pos]
        # 重新进行堆化
        length -= 1
        heapify(alist, length, 0)


def heapify(alist, length, pos):
    max_pos = pos
    while True:
        # 找到 大于 pos 节点的最大孩子节点位置
        if (pos * 2 + 1) < length and alist[pos] < alist[pos * 2 + 1]:
            max_pos = pos * 2 + 1
        if (pos * 2 + 2) < length and alist[max_pos] < alist[pos * 2 + 2]:
            max_pos = pos * 2 + 2
        if (pos == max_pos):
            break
        alist[pos], alist[max_pos] = alist[max_pos], alist[pos]
        pos = max_pos


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    # quick_sort(a)
    heap_sort(a)
    print(a)
