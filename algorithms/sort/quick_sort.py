# 快速排序


def quick_sort(alist):
    left = 0
    right = len(alist) - 1
    sort(alist, left, right)



def sort(alist, left, right):
    if left >= right:
        return
    pivot = partition(alist, left, right)
    sort(alist, left, pivot-1)
    sort(alist, pivot+1, right)


def partition(alist, left, right):
    # 以 alist[right] 作为分区值
    i = left
    for j in range(left, right):
        if alist[j] < alist[right]:
            alist[i] , alist[j] = alist[j], alist[i]
            i += 1
    alist[i], alist[right] = alist[right], alist[i]
    # 以 alist[left] 作为分区点
    # i = right
    # for j in range(right, left, -1):
    #     if alist[j] > alist[left]:
    #         alist[j], alist[i] = alist[i], alist[j]
    #         i -= 1
    # alist[i], alist[left] = alist[left], alist[i]
    print(alist)
    print(left, i, right)
    return i


# 利用快排思想求解无序数组中的第 K 大元素
def big_k(alist, k):
    left = 0
    right = len(alist) - 1
    p = find_k(alist, left, right, k)
    return alist[p]


def find_k(alist, left, right, k):
    pivot = partition(alist, left, right)
    if len(alist) - pivot == k:
        return pivot
    if len(alist) - pivot > k:
        return find_k(alist, pivot+1, right, k)
    else:
        return find_k(alist, left, pivot-1, k)


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    # quick_sort(a)
    k = big_k(a, 4)
    print(k)
