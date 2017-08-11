from graphTraversal import *
import unittest
import numpy as np


node0 = Node([0, 0, 0], "Hotel")
node1 = Node([1, 1.5, 1], "1")
node2 = Node([2, 0.5, 2], "2")
node3 = Node([3, 2.5, 3], "3")
node4 = Node([4, 3.5, 4], "4")
times = np.array([[0,1,4,2,3],[1,0,7,1,10],[4,7,0,8,11],[2,1,8,0,0.5],[3,10,11,0.5,0]])

class TestStringMethods(unittest.TestCase):

    def test_add(self):
        x = DoubleList(times)
        x.add(node0)
        self.assertEqual(x.profit,0)
        self.assertEqual(x.duration,0)
        x.add(node1)
        self.assertEqual(x.profit, 1.5)
        self.assertEqual(x.duration, 3)
        x.add(node2)
        self.assertEqual(x.profit, 2)
        self.assertEqual(x.duration, 15)
        x.add(node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)

    def test_switch(self):
        x = DoubleList(times)
        x.add(node0)
        x.add(node1)
        x.add(node2)
        x.add(node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)
        x.switch(node3, node4)
        self.assertEqual(x.profit, 5.5)
        self.assertEqual(x.duration, 29)
        x.switch(node4, node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)


    def test_independent(self):
        x = DoubleList(times)
        y = DoubleList(times)
        x.add(node0)
        x.add(node1)
        x.add(node2)
        x.add(node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)
        x.switch(node3, node4)
        self.assertEqual(y.profit, 0)
        self.assertEqual(y.duration, 0)

    def test_relocate(self):
        x = DoubleList(times)
        x.add(node0)
        x.add(node1)
        x.add(node2)
        x.add(node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)
        x.relocate(node3, node1)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 20)
        x.relocate(node3, node2)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)

    def test_swap(self):
        x = DoubleList(times)
        x.add(node0)
        x.add(node1)
        x.add(node2)
        x.add(node3)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)
        x.swap(node3, node2)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 20)
        x.swap(node3, node2)
        self.assertEqual(x.profit, 4.5)
        self.assertEqual(x.duration, 24)


if __name__ == '__main__':
    unittest.main()