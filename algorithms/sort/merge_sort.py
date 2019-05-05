# 归并排序
# 使用分而治之的思想，
# 先把数组从中间分成前后两部分，然后对前后两部分分别排序，再将排好序的两部分合并在一起。


def merge_sort(alist):
    length = len(alist)
    if length <= 1:
        return alist
    middle = length // 2
    left = merge_sort(alist[:middle])
    right = merge_sort(alist[middle:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # 使用等号，以保证是稳定排序
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    if i == len(left):
        result.extend(right[j:])
    else:
        result.extend(left[i:])
    return result


if __name__ == '__main__':
    a = [2, 1, 5, 4, 6, 3]
    r = merge_sort(a)
    print(r)
