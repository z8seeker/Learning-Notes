# -*- coding:utf-8 -*-
# 输入两棵二叉树A，B，判断B是不是A的子结构。（ps：我们约定空树不是任意一个树的子结构）

# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def HasSubtree(self, pRoot1, pRoot2):
        # write code here
        if pRoot1 is None or pRoot2 is None:
            return False
        
        if self.isSubtree(pRoot1, pRoot2):
            return True
        if self.HasSubtree(pRoot1.left, pRoot2):
            return True
        if self.HasSubtree(pRoot1.right, pRoot2):
            return True

        return False
        
    def isSubtree(self, node1, node2):
        if node2 is None:
            return True
        if node1 is None:
            return False
        if node1.val == node2.val:
            return self.isSubtree(node1.left, node2.left) and self.isSubtree(node1.right, node2.right)
        else:
            return False
  