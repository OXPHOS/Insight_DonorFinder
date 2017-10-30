import unittest
from src.AVLTree import *
from src import InfoByDate, LinkedListNode


class TestAVLTree(unittest.TestCase):
    def test_nodeByDate_comparison(self):
        date1 = '01022017'
        date2 = '10312000'
        date3 = '02292016'
        info = InfoByDate(LinkedListNode(40.0))
        node1 = NodeByDate(date1, info)
        node2 = NodeByDate(date2, info)
        node3 = NodeByDate(date3, info)
        self.assertTrue(node1 > node2)
        self.assertTrue(node1 > node3)
        self.assertTrue(node2 < node3)

    def test_nodeByID_comparison(self):
        id1 = 'C00629618'
        id2 = 'C10629618'
        id3 = 'C00629618'
        date = '01022017'
        info = InfoByDate(LinkedListNode(40.0))
        node1 = NodeByID(id1, date, info)
        node2 = NodeByID(id2, date, info)
        node3 = NodeByID(id3, date, info)
        self.assertTrue(node1 < node2)
        self.assertTrue(node1 == node3)

    def test_nodeByID_update_on_same_date(self):
        id = 'C00629618'
        date = '01022017'
        amt = LinkedListNode(40.0)
        info1 = InfoByDate(amt)  # 40, 1, 40.0
        node1 = NodeByID(id, date, info1)

        res = node1.val.root.val
        self.assertIsInstance(res, InfoByDate)
        self.assertEqual(res.get_median(), 40)
        self.assertEqual(res.get_count(), 1)
        self.assertAlmostEqual(res.get_total(), 40)

        info2 = InfoByDate(LinkedListNode(60.5))  # 61, 1, 60.5
        info2.update(amt)  # 50, 2, 100.5
        node2 = NodeByID(id, date, info2)
        node1.update_node(node2)

        res = node1.val.root.val
        self.assertIsInstance(res, InfoByDate)
        self.assertEqual(res.get_median(), 50)
        self.assertEqual(res.get_count(), 2)
        self.assertAlmostEqual(res.get_total(), 100.5)

    def test_nodeByID_update_on_different_date(self):
        id = 'C00629618'
        date1 = '01022017'
        date2 = '10312000'
        info1 = InfoByDate(LinkedListNode(40.0))  # 40, 1, 40.0
        node1 = NodeByID(id, date1, info1)
        info2 = InfoByDate(LinkedListNode(60.5))  # 61, 1, 60.5
        node2 = NodeByID(id, date2, info2)
        node1.update_node(node2)

        res = node1.val.root
        self.assertIsInstance(res, NodeByDate)
        self.assertEqual(res.val.get_median(), 40)
        self.assertEqual(res.val.get_count(), 1)
        self.assertAlmostEqual(res.val.get_total(), 40)

        # node2 - append as left child of node2
        self.assertIsInstance(res.left, NodeByDate)
        self.assertEqual(res.left.val.get_median(), 61)
        self.assertEqual(res.left.val.get_count(), 1)
        self.assertAlmostEqual(res.left.val.get_total(), 60.5)

        self.assertIsNone(res.right)

    # TODO: Test AVL tree implementation.
    # The construct of tree has been tested with simple date type
    # for eg. AVL tree with int as key and value
