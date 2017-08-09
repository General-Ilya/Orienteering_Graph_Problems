import numpy as np

class Node(object):
    def __init__(self, data, name, prev=None, next=None):
        self.name = name
        self.data = data
        self.prev = prev
        self.next = next
    def print(self):
        print(self.prev.name)# if hasattr(self.name, "data") else None)
        print(self.data, self.name)
        print(self.next.name)# if hasattr(self.name, "data") else None)


class DoubleList(object):
    tail = None # The first added node
    head = None # The newest added node
    duration = 0
    profit = 0
    size = 0

    def print(self):
        curr = self.tail
        print("---")
        for i in range(self.size):
            curr.print()
            print("---")
            curr = curr.next
        print("***")

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
        if (dead_node is self.tail):
            self.tail = new_node
        if (dead_node is self.head):
            self.head = new_node
        dead_node.prev.next = new_node
        new_node.prev = dead_node.prev

        self.size -= 1

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
        if self.size == 0:
            self.tail = self.head = node
        else:
            node.prev = self.head
            node.next = self.tail
            node.prev.next = node
            node.next.prev = node
            self.head = node
        self.size += 1

    # Swap node with name for new_node in place
    def switchTry(self, old_node, new_node):
        name = old_node.name
        switched_node = self.get(name)
        orig = [switched_node.prev, switched_node, switched_node.next]
        new = [switched_node.prev, new_node, switched_node.next]
        return evalDifference(orig, new)

    def switch(self, old_node, new_node):
        self.updateTrip(self.switchTry(old_node, new_node))
        name = old_node.name
        dead_node = self.get(name)
        if(dead_node is self.tail):
            self.tail = new_node
        if (dead_node is self.head):
            self.head = new_node
        new_node.prev = dead_node.prev
        new_node.next = dead_node.next
        dead_node.prev.next = new_node
        dead_node.next.prev = new_node



    def relocateTry(self, node_first, node_second):
        return [0,0]

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
        if self.size <=1:
            return [0,0]
        orig = []
        new = []
        curr = old_node.prev
        while curr != new_node.next:
            orig.append(curr)
            if curr is old_node:
                new.append(new_node)
            elif curr is new_node:
                new.append(old_node)
            else:
                new.append(curr)
            curr = curr.next
        orig.append(new_node.next)
        new.append(new_node.next)
        return evalDifference(orig, new)

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
    for i in range(len(nodes)-1):
        retVal += time(nodes[i], nodes[i+1])
    return retVal

def time(nodeA, nodeB):
    t = times[nodeA.data[0]][nodeB.data[0]] + nodeA.data[2]
    return t

def profit(node):
    return node.data[1]

# Testing
# Node
# [name, profit, time_to_complete]

node0 = Node([0, 0, 0], "Hotel")
node1 = Node([1, 1.5, 6], "1")
node2 = Node([2, 0.5, 15], "2")
node3 = Node([3, 2.5, 12], "3")
node4 = Node([4, 3.5, 7], "4")
times = np.array([[0,1,4,2,3],[1,0,7,1,10],[4,7,0,8,11],[2,1,8,0,0.5],[3,10,11,0.5,0]])

x = DoubleList()
x.add(node0)
x.add(node1)
x.add(node2)
x.add(node3)
x.add(node4)
x.print()
x.swap(node1, node4)
x.print()