# 插入排序
# 将数组中的数据分为两个区间：已排序区间和未排序区间，
# 然后取未排序区间中的元素在已排序区间中找到合适的插入位置将其插入，
# 保证已排序区间一直是有序的。重复这个过程直到未排序区间中的元素为空。


def insert_sort(alist):
    length = len(alist)
    for i in range(1, length):
        value = a[i]
        # 从尾到头查找插入点
        j = i - 1
        while j >= 0 and (a[j] > value):
            a[j + 1] = a[j]
            j -= 1
        a[j+1] = value
        # 从头到尾查找插入点
        # for j in range(0, i):
        #     if a[j] > a[i]:
        #         for k in range(i, j, -1):
        #             a[k] = a[k-1]
        #         a[j] = value


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    insert_sort(a)
    print(a)
