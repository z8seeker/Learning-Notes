# circular list example
# josephus problem

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    

def main(m, n):
    head = tail = Node(1)
    head.next = head
    for i in range(2, n+1):
        tail.next = Node(i)
        tail = tail.next
        tail.next = head
    
    node = tail
    while node is not node.next:
        for i in range(1, m):
            node = node.next
        # drop next
        node.next = node.next.next
    
    print(node.value)
    

if __name__ == '__main__':

    main(3, 5)
