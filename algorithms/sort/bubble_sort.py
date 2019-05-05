# 冒泡排序
# 只操作相邻的两个数据，一次冒泡会让至少一个元素移动到它应该在的位置，
# 当某次冒泡操作已经没有数据交换时，就说明已经达到完全有序了。


def bubble_sort(alist):
    length = len(alist)
    if length < 2:
        return
    for i in range(length):
        flag = True
        for j in range(0, length - i - 1):
            if alist[j + 1] < alist[j]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                flag = False
        if flag:
            break


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    bubble_sort(a)
    print(a)
