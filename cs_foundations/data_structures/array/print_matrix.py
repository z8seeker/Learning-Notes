# -*- coding:utf-8 -*-
# 输入一个矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字，
# 例如，如果输入如下4 X 4矩阵： 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 
# 则依次打印出数字1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,10.


class Solution:
    # matrix类型为二维列表，需要返回列表
    def printMatrix(self, matrix):
        # write code here
        result = []
        while matrix:
            result += matrix.pop(0)
            matrix = zip(*matrix)[::-1]
        return result
            


# -*- coding:utf-8 -*-
class Solution:
    # matrix类型为二维列表，需要返回列表
    result = []
    def printMatrix(self, matrix):
        # write code here
        top = left = 0
        
        bottom = len(matrix) - 1
        right = len(matrix[0]) - 1
        self.traversal(matrix, top, bottom, left, right)
        
        return self.result
    
    def traversal(self, matrix, top, bottom, left, right):
        if top > bottom:
            return
        if left > right:
            return
        if len(matrix) > 1:
            if top == bottom:
                for i in range(left, right+1):
                    self.result.append(matrix[top][i])
            if left == right:
                for i in range(top, bottom+1):
                    self.result.append(matrix[i][left])
        else:
            for i in matrix[0]:
                self.result.append(i)
                return
        
        self.printClockWise(matrix, top, bottom, left, right)
        self.traversal(matrix, top+1, bottom-1, left+1, right-1)
    
    def printClockWise(self, matrix, top, bottom, left, right):
        for i in range(top, right+1):
            self.result.append(matrix[top][i])
        for i in range(top+1, bottom):
            self.result.append(matrix[i][right])
        for i in range(right, left-1, -1):
            self.result.append(matrix[bottom][i])
        for i in range(bottom-1, top, -1):
            self.result.append(matrix[i][left])
            