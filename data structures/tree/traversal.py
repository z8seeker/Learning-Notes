# 二叉树的遍历

# 前序遍历：对于任意节点，先打印这个节点，然后打印它的左子树，最后打印它的右子树
# 中序遍历：对于任意节点，先打印这个节点的左子树，再打印这个节点，最后打印这个节点的右子树
# 后序遍历：对于任意节点，先打印这个节点的左子树，再打印这个节点的右子树，最后打印这个节点
# 层序遍历：从第一层开始依次从左到右遍历全部的节点

class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = self.right = None


def pre_order(root: Node):
    if root is None:
        return
    print(root.value)
    pre_order(root.left)
    pre_order(root.right)


def in_order(root: Node):
    if root is None:
        return
    in_order(root.left)
    print(root.value)
    in_order(root.right)


def post_order(root: Node):
    if root is None:
        return
    post_order(root.left)
    post_order(root.right)
    print(root.value)


def level_order(root: Node):
    from collections import deque
    dq = deque()
    dq.append(root)
    while dq:
        node = dq.popleft()
        if node is not None:
            print(node.value)
            dq.append(node.left)
            dq.append(node.right)


def tree_height(root: Node):
    if root is None:
        return 0
    else:
        return max(tree_height(root.left), tree_height(root.right)) + 1


if __name__ == '__main__':
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.right = Node(4)
    h = tree_height(root)
    print(h)
    level_order(root)
