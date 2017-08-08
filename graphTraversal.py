import numpy as np

class Node(object):
    def __init__(self, data, name, prev=None, next=None):
        self.name = name
        self.data = data
        self.prev = prev
        self.next = next
    def print(self):
        print(self.data, self.name)

class DoubleList(object):
    tail = None
    head = None
    size = 0

    # Add node to end of List
    def add(self, node):
        if self.size == 0:
            self.tail = self.head = node
        else:
            node.prev = self.head
            node.next = self.tail
            node.prev.next = node
            node.next.prev = node
            self.head = node
        self.size += 1

    def print(self):
        curr = self.tail
        print("---")
        for i in range(self.size):
            curr.print()
            print("---")
            curr = curr.next
        print("***")

    # Swap node with name for new_node in place
    def switch(self, name, new_node):
        dead_node = self.get(name)
        if(dead_node is self.tail):
            self.tail = new_node
        if (dead_node is self.head):
            self.head = new_node
        new_node.prev = dead_node.prev
        new_node.next = dead_node.next
        dead_node.prev.next = new_node
        dead_node.next.prev = new_node

    # Return node with name if found, else throw error
    def get(self, name):
        curr = self.tail
        for i in range(self.size):
            if curr.name == name:
                return curr
            curr = curr.next
        raise Exception("Node not Found/Node Pas Trouvé")

    # Remove node with name, in place
    def remove(self, name):
        if self.size == 0:
            raise Exception("Empty list")
        if self.size == 1:
            self.size = 0
            self.tail = None
            self.head = None
            return
        dead_node = self.get(name)
        new_node = dead_node.next
        if(dead_node is self.tail):
            self.tail = new_node
        if (dead_node is self.head):
            self.head = new_node
        dead_node.prev.next = new_node
        new_node.prev = dead_node.prev

        self.size -= 1


x = DoubleList()
x.add(Node(3, 'Poisson'))
x.add(Node(4, 1))
x.add(Node(5, 2))
x.print()
x.switch('Poisson', Node(42, 'Fish'))
x.print()
x.add(Node(12, "Chicken"))
x.print()
x.switch("Chicken", Node(33, "Poulet"))
x.print()
x.remove("Poulet")
x.print()
x.remove(2)
x.print()
x.remove(1)
x.print()
x.remove("Fish")
x.print()
print(x.size)