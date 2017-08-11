import numpy as np


class Node(object):
    def __init__(self, data, name, prev=None, next=None):
        self.name = name
        self.data = data
        self.prev = prev
        self.next = next

    def display(self):
        print(self.prev.name)
        print(self.data, self.name)
        print(self.next.name)


class DoubleList(object):
    def __init__(self, times):
        self.tail = None  # The first added node
        self.head = None  # The newest added node
        self.duration = 0
        self.profit = 0
        self.times = times

    def display(self):
        curr = self.tail
        print("---")
        curr.display()
        print("---")
        curr = curr.next
        while curr is not self.tail:
            curr.display()
            print("---")
            curr = curr.next
        print("***")

    # Return node with name if found, else throw error
    def get(self, name):
        curr = self.tail
        if curr.name == name:
            return curr
        curr = curr.next
        while curr is not self.tail:
            if curr.name == name:
                return curr
            curr = curr.next
        return None

    # Remove node with name, in place
    def remove(self, node):
        name = node.name
        if self.tail == None or self.head == None:
            raise Exception("Empty list")
        if self.tail is self.head:
            self.tail = None
            self.head = None
            return
        dead_node = self.get(name)
        new_node = dead_node.next
        if (dead_node is self.tail):
            self.tail = new_node
        if (dead_node is self.head):
            self.head = new_node
        dead_node.prev.next = new_node
        new_node.prev = dead_node.prev

    def updateTrip(self, change):
        self.duration += change[1]
        self.profit += change[0]

    # Add node to end of List
    def addTry(self, node):
        if self.head is None:
            return evalDifference([], [node])
        return evalDifference([self.head, self.tail, self.head], [self.head, node, self.tail, self.head])

    def add(self, node):
        self.updateTrip(self.addTry(node))
        if self.head is None or self.tail is None:
            self.tail = self.head = node
        else:
            node.prev = self.head
            node.next = self.tail
            node.prev.next = node
            node.next.prev = node
            self.head = node

    # Swap node with name for new_node in place
    def switchTry(self, old_node, new_node):
        switched_node = old_node
        orig = [switched_node.prev, switched_node, switched_node.next]
        new = [switched_node.prev, new_node, switched_node.next]
        return evalDifference(orig, new)

    def switch(self, old_node, new_node):
        self.updateTrip(self.switchTry(old_node, new_node))
        dead_node = old_node
        if (dead_node is self.tail):
            raise Exception("Hotel")
        if (dead_node is self.head):
            self.head = new_node
        new_node.prev = dead_node.prev
        new_node.next = dead_node.next
        dead_node.prev.next = new_node
        dead_node.next.prev = new_node

    def relocateTry(self, node_first, node_second):
        orig1 = [node_first, node_first.next]
        new1 = [node_first, node_second, node_first.next]
        orig2 = [node_second.prev, node_second, node_second.next]
        new2 = [node_second.prev, node_second.next]
        d1 = evalDifference(orig1, new1)
        d2 = evalDifference(orig2, new2)
        return [d1[0] + d2[0], d1[1] + d2[1]]

    def relocate(self, node_first, node_second):
        self.updateTrip(self.relocateTry(node_first, node_second))
        node_second.next.prev = node_second.prev
        node_second.prev.next = node_second.next
        node_first.next.prev = node_second
        node_second.next = node_first.next
        node_first.next = node_second
        node_second.prev = node_first
        node_first.next = node_second

    def swapTry(self, old_node, new_node):
        # Special case if they're adjacent
        if old_node.next is new_node:
            ori = [old_node.prev, old_node, new_node, new_node.next]
            new = [old_node.prev, new_node, old_node, new_node.next]
            return evalDifference(ori, new)
        elif new_node.next is old_node:
            ori = [new_node.prev, new_node, old_node, old_node.next]
            new = [new_node.prev, old_node, new_node, old_node.next]
            return evalDifference(ori, new)

        orig1 = [old_node.prev, old_node, old_node.next]
        new1 = [old_node.prev, new_node, old_node.next]
        orig2 = [new_node.prev, new_node, new_node.next]
        new2 = [new_node.prev, old_node, new_node.next]
        d1 = evalDifference(orig1, new1)
        d2 = evalDifference(orig2, new2)
        return [d1[0] + d2[0], d1[1] + d2[1]]

    # Brute force swap, consider fixing
    def swap(self, old_node, new_node):
        self.updateTrip(self.swapTry(old_node, new_node))
        s1 = old_node.name
        s2 = old_node.data
        old_node.name = new_node.name
        old_node.data = new_node.data
        new_node.name = s1
        new_node.data = s2


def evalDifference(nodes_orig, nodes_new):
    dt = evalProfit(nodes_new) - evalProfit(nodes_orig)
    dr = evalTime(nodes_new) - evalTime(nodes_orig)
    return [dt, dr]


def evalProfit(nodes):
    retVal = 0
    for node in nodes:
        retVal += profit(node)
    return retVal


def evalTime(nodes):
    retVal = 0
    for i in range(len(nodes) - 1):
        retVal += time(nodes[i], nodes[i + 1])
    return retVal


def time(nodeA, nodeB):
    t = times[nodeA.data[0]][nodeB.data[0]] + nodeA.data[2]
    return t


def profit(node):
    return node.data[1]


# Testing
# Node
# [name, profit, time_to_complete]

node0 = Node([0, 0, 0], "Hotel1")
node00 = Node([0, 0, 0], "Hotel2")
node1 = Node([1, 1.5, 0], "1")
node2 = Node([2, 0.5, 0], "2")
node3 = Node([3, 2.5, 0], "3")
node4 = Node([4, 3.5, 0], "4")
times = np.array([[0, 1, 4, 2, 3], [1, 0, 7, 1, 10], [4, 7, 0, 8, 11], [2, 1, 8, 0, 0.5], [3, 10, 11, 0.5, 0]])

x = DoubleList(times)
x.add(node0)
x.add(node1)
x.add(node2)

y = DoubleList(times)
y.add(node00)
y.add(node3)
y.add(node4)

print("X")
x.display()

print("Y")
y.display()

x.relocate(node2, node4)

print("X")
x.display()

print("Y")
y.display()