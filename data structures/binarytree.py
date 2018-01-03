"""
list of lists representations
"""


# tree-making functions
def binary_tree(r):
    return [r, [], []]


# inserting a left child
def insert_left(root, new_branch):
    t = root.pop(1)
    if len(t) > 1:
        root.insert(1, [new_branch, t, []])
    else:
        root.insert(1, [new_branch, [], []])
    return root


# inserting a right child
def insert_right(root, new_branch):
    t = root.pop(2)
    if len(t) > 1:
        root.insert(2, [new_branch, [], t])
    else:
        root.insert(2, [new_branch, [], []])
    return root


def root_value(root):
    return root[0]


def set_root_value(root, value):
    root[0] = value


def left_child(root):
    return root[1]


def right_child(root):
    return root[2]


def build_tree():
    r = binary_tree('a')
    insert_left(r, 'b')
    insert_right(r, 'c')
    insert_right(left_child(r), 'd')
    insert_left(right_child(r), 'e')
    insert_right(right_child(r), 'f')
    return r


"""
implement using nodes and references
"""


class BinaryTree:
    def __init__(self, payload):
        self.key = payload
        self.left_child = None
        self.right_child = None

    def insert_left(self, value):
        if self.left_child is None:
            self.left_child = BinaryTree(value)
        else:
            t = BinaryTree(value)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, value):
        if self.right_child is None:
            self.right_child = BinaryTree(value)
        else:
            t = BinaryTree(value)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_value(self, value):
        self.key = value

    def get_root_value(self):
        return self.key
