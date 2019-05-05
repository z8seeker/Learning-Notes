# 选择排序
# 选择排序也分已排序区间和未排序区间，
# 每次从未排序区间中找到最小的元素，将其放到已排序区间的末尾。


def selection_sort(alist):
    length = len(alist)
    for i in range(length - 1):
        min_index = i
        for j in range(i + 1, length):
            if alist[j] < alist[min_index]:
                min_index = j
        alist[i], alist[min_index] = alist[min_index], alist[i]


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    selection_sort(a)
    print(a)
