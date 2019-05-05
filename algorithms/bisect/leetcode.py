# 33, 循环有序数组

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low = 0
        high = len(nums) - 1
        return self.search_c(nums, low, high, target)

    def search_c(self, nums, low, high, target):
        if low > high:
            return -1
        
        mid = (low + high) // 2
        if nums[low] <= nums[mid]:
            r = self.bsearch(nums, low, mid, target)
            if r is not None:
                return r
            else:
                return self.search_c(nums, mid+1, high, target)
        else:
            r = self.bsearch(nums, mid, high, target)
            if r is not None:
                return r
            else:
                return self.search_c(nums, low, mid-1, target)
    
    def bsearch(self, nums, low, high, target):
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                high = mid - 1
            else:
                low = mid + 1


if __name__ == '__main__':
    a = [3, 1]
    r = Solution().search(a, 1)
    print(r)
