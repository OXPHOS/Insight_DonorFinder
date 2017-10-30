import unittest
from src import LinkedListNode


class TestLinkedListNode(unittest.TestCase):
    def test_constructor(self):
        mid_node = LinkedListNode(5)
        self.assertEqual(mid_node.get_value(), 5)
        self.assertIsNone(mid_node.left)
        self.assertIsNone(mid_node.right)

    def test_neighboring(self):
        # Move around 3 nodes
        left_node = LinkedListNode(1)
        right_node = LinkedListNode(9)
        mid_node = LinkedListNode(5, left_node, right_node)
        left_node.right, right_node.left = mid_node, mid_node

        self.assertEqual(right_node.left.left.get_value(), left_node.get_value())
        self.assertIsNone(right_node.right)
        self.assertEqual(right_node.left, left_node.right)

    def test_node_insertaion(self):
        # Insert a new node in linked list
        size = 6
        node = [None] * size
        node[0] = LinkedListNode(0)
        for i in xrange(1, size):
            node[i] = LinkedListNode(i, node[i-1])
        for i in xrange(0, size-1):
            node[i].right = node[i+1]

        new_node = LinkedListNode(4.5)
        LinkedListNode.insert_linkedlist_node(node[0], new_node, 'r')

        self.assertIs(new_node.left, node[4])
        self.assertIs(new_node.right, node[5])
        self.assertIs(node[5].left, new_node)
        self.assertIs(node[4].right, new_node)
