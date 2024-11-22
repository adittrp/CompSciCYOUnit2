from listnode import Node


class LinkedList:
    def __init__(self):
        self.head = None

    def addNode(self, desc, priority, time):
        if self.head is None:
            self.head = Node(desc, priority, time, None)
            return self.head
        else:
            node = self.head
            while node.next is not None:
                node = node.next

            node.next = Node(desc, priority, time, None)
            return node.next

    def removeNode(self, desc=None):
        node = self.head
        previous = None

        while node is not None:
            if desc == node.description:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next
                break

            previous = node
            node = node.next
