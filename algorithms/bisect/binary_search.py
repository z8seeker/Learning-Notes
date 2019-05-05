# 二分查找算法
# 最简单的情况：有序数组中不存在重复元素


def binary_search(alist, target):
    low = 0
    high = len(alist) - 1
    while low <= high:
        mid = (low + high) // 2
        if alist[mid] == target:
            return mid
        elif alist[mid] > target:
            high = mid - 1
        else:
            low = mid + 1


def binary_search_first(alist, target):
    low = 0
    high = len(alist) - 1
    while low <= high:
        mid = (low + high) // 2
        if alist[mid] == target:
            if (mid == 0 or alist[mid-1] != target):
                return mid
            else:
                high = mid - 1
        elif alist[mid] > target:
            high = mid - 1
        else:
            low = mid + 1


def binary_search_last(alist, target):
    low = 0
    high = len(alist) - 1
    while low <= high:
        mid = (low + high) // 2
        if alist[mid] == target:
            if (mid == len(alist) - 1 or alist[mid+1] != target):
                return mid
            else:
                low = mid + 1
        elif alist[mid] > target:
            high = mid - 1
        else:
            low = mid + 1


def bsearch_first_gte(alist, target):
    low = 0
    high = len(alist) - 1
    while low <= high:
        mid = (low + high) // 2
        if alist[mid] >= target:
            if (mid == 0 or alist[mid-1] < target):
                return mid
            high = mid - 1
        else:
            low = mid + 1


def bsearch_last_lte(alist, target):
    low = 0
    high = len(alist) - 1
    while low <= high:
        mid = (low + high) // 2
        if alist[mid] <= target:
            if (mid == len(alist) - 1 or alist[mid+1] > target):
                return mid
            low = mid + 1
        else:
            low = mid - 1


# 使用递归实现
def bsearch(alist, target):
    low = 0
    high = len(alist) - 1
    return search(alist, low, high, target)


def search(alist, low, high, target):
    if low > high:
        return
    mid = (low + high) // 2
    if alist[mid] == target:
        return mid
    elif alist[mid] > target:
        return search(alist, low, mid-1, target)
    else:
        return search(alist, mid+1, high, target)


if __name__ == '__main__':
    a = [1, 1, 1, 2, 4, 4, 5, 5, 6, 6]
    # r = binary_search_last(a, 5)
    r = bsearch_first_gte(a, 2)
    # r = bsearch(a, 99)
    print(r)
