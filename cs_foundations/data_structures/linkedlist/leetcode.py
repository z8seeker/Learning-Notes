# 单链表反转 206, 
# 链表中环的检测 141, 
# 两个有序的链表合并 21, 
# 删除链表倒数第 n 个结点 19, 
# 求链表中的中间结点 876

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class solution206(object):
    # 方法 1， 过程直接
    def reverseList(self, head):
        node = head
        prev = None
        while node is not None:
            next_node = node.next
            node.next = prev
            prev = node
            node = next_node
    
    # 方法 1， 改进版 1
    def reverseList1(self, head):
        prev = None
        while head:
            curr = head
            head = head.next
            curr.next = prev
            prev = curr
    
    # 方法 1，改进版 2
    def reverseList12(self, head):
        curr, prev = head, None
        while curr:
            curr.next, prev, curr = prev, curr, curr.next
        return prev
    
    # 方法 2，头插法
    def reverseList2(self, head):
        if head is None:
            return head
        new_head = head
        while head.next is not None:
            current = head.next
            head.next = head.next.next
            current.next = new_head
            new_head = current
    
    # 方法 3，使用递归
    def reverseList3(self, head, prev=None):
        if head is None:
            return prev
        curr, head.next = head.next, prev
        return self.reverseList3(curr, head)


class Solution141(object):
    def hasCycle(self, head):
        fast = slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                return True
        return False
