import unittest
from src import LinkedListNode
from src.InfoTable import *


class TestInfoByDomainBase(unittest.TestCase):
    def test_contructor(self):
        node = LinkedListNode(4.7)
        info = InfoByDomainBase(node)

        self.assertEqual(info.get_median(), 5)  # round-up
        self.assertEqual(info.get_count(), 1)
        self.assertAlmostEqual(info.get_total(), 4.7)
        self.assertAlmostEqual(info.get_median_left().get_value(), 4.7)
        self.assertIs(info.get_median_left(), info.get_median_right())

    def test_update_from_empty_info(self):
        info = InfoByDomainBase(None)
        node = LinkedListNode(4.7)
        info.update(node)

        self.assertEqual(info.get_median(), 5)  # round-up
        self.assertEqual(info.get_count(), 1)
        self.assertAlmostEqual(info.get_total(), 4.7)
        self.assertAlmostEqual(info.get_median_left().get_value(), 4.7)
        self.assertIs(info.get_median_left(), info.get_median_right())

    def test_update(self):
        source_node = LinkedListNode(10)
        info = InfoByDomainBase(source_node)

        # Raise error if repeatedly adding one transaction
        self.assertRaises(RuntimeError, lambda : info.update(source_node))

        # Amount <= current median and amount <= median.left,
        # and median_left is median_right
        info.update(LinkedListNode(5))
        self.assertEqual(info.get_median(), 8)
        self.assertEqual(info.get_count(), 2)
        self.assertAlmostEqual(info.get_total(), 15)
        self.assertAlmostEqual(info.get_median_left().get_value(), 5)
        self.assertAlmostEqual(info.get_median_right().get_value(), 10)

        # Amount > current median, and amount > median_right
        # and median_left is not median_right
        info.update(LinkedListNode(30))
        self.assertEqual(info.get_median(), 10)
        self.assertEqual(info.get_count(), 3)
        self.assertAlmostEqual(info.get_total(), 45)
        self.assertAlmostEqual(info.get_median_left().get_value(), 10)
        self.assertAlmostEqual(info.get_median_right().get_value(), 10)

        # Amount > current median, and amount > median_right
        # and median_left is median_right
        info.update(LinkedListNode(40))
        self.assertEqual(info.get_median(), 20)
        self.assertEqual(info.get_count(), 4)
        self.assertAlmostEqual(info.get_total(), 85)
        self.assertAlmostEqual(info.get_median_left().get_value(), 10)
        self.assertAlmostEqual(info.get_median_right().get_value(), 30)

        # Amount > current median, but amount <= median_right
        # and median_left is not median_right
        info.update(LinkedListNode(25))
        self.assertEqual(info.get_median(), 25)  # round-up
        self.assertEqual(info.get_count(), 5)
        self.assertAlmostEqual(info.get_total(), 110)
        self.assertAlmostEqual(info.get_median_left().get_value(), 25)
        self.assertAlmostEqual(info.get_median_right().get_value(), 25)

        # Amount <= current median, but amount > median_left
        # and median_left is not median_right
        info.update(LinkedListNode(10))
        info.update(LinkedListNode(17))
        self.assertEqual(info.get_median(), 17)  # round-up
        self.assertEqual(info.get_count(), 7)
        self.assertAlmostEqual(info.get_total(), 137)
        self.assertAlmostEqual(info.get_median_left().get_value(), 17)
        self.assertAlmostEqual(info.get_median_right().get_value(), 17)

        # Amount <= current median, and amount <= median_left
        # and median_left is not median_right
        info.update(LinkedListNode(1))
        info.update(LinkedListNode(2))
        self.assertEqual(info.get_median(), 10)  # round-up
        self.assertEqual(info.get_count(), 9)
        self.assertAlmostEqual(info.get_total(), 140)
        self.assertAlmostEqual(info.get_median_left().get_value(), 10)
        self.assertAlmostEqual(info.get_median_right().get_value(), 10)

    def test_update_floats(self):
        nodes = map(LinkedListNode, [1, 3.3, 2, 4.5, 1.8, 6])
        info = InfoByDomainBase(nodes[0])
        for i in xrange(1, 6):
            info.update(nodes[i])

        self.assertEqual(info.get_median(), 3)  # round-up
        self.assertEqual(info.get_count(), 6)
        self.assertAlmostEqual(info.get_total(), 18.6)
        self.assertAlmostEqual(info.get_median_left().get_value(), 2)
        self.assertAlmostEqual(info.get_median_right().get_value(), 3.3)


class TestInfoIndividual(unittest.TestCase):
    def test_contructor(self):
        zip = '90017'
        date = '01032017'
        record = {'CMTE_ID': 'C00629618', 'TRANSACTION_AMT': LinkedListNode(40.0),
               'ZIP_CODE': zip, 'TRANSACTION_DT': date}
        id = InfoIndividual(record)

        self.assertTrue(id.has_zip(zip))
        self.assertTrue(id.has_date(date))
        self.assertIsNotNone(id.get_zip_dict_entry(zip))
        self.assertIsNotNone(id.get_date_dict_entry(date))

        self.assertIsNone(id.get_zip_dict_entry(""))
        self.assertIsNone(id.get_date_dict_entry(""))

    def test_same_zip_update(self):
        id = 'C00629618'
        zip = '90017'
        amt1 = LinkedListNode(40.0)
        amt2 = LinkedListNode(60.5)
        record1 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt1, 'ZIP_CODE': zip}
        record2 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt2, 'ZIP_CODE': zip}

        id = InfoIndividual(record1)
        id.update_by_zip(record2)
        info_zip = id.get_zip_dict_entry(zip)

        self.assertEqual(info_zip.get_median(), 50)
        self.assertEqual(info_zip.get_count(), 2)
        self.assertAlmostEqual(info_zip.get_total(), 100.5)

    def test_different_zip_update(self):
        id = 'C00629618'
        zip1 = '90017'
        zip2 = '10021'
        amt1 = LinkedListNode(40.0)
        amt2 = LinkedListNode(60.5)
        record1 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt1, 'ZIP_CODE': zip1}
        record2 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt2, 'ZIP_CODE': zip2}

        id = InfoIndividual(record1)
        id.update_by_zip(record2)
        info_zip1 = id.get_zip_dict_entry(zip1)
        info_zip2 = id.get_zip_dict_entry(zip2)

        self.assertEqual(info_zip1.get_median(), 40)
        self.assertEqual(info_zip1.get_count(), 1)
        self.assertAlmostEqual(info_zip1.get_total(), 40)

        self.assertEqual(info_zip2.get_median(), 61)
        self.assertEqual(info_zip2.get_count(), 1)
        self.assertAlmostEqual(info_zip2.get_total(), 60.5)

    def test_same_date_update(self):
        id = 'C00629618'
        date = '01022017'
        amt1 = LinkedListNode(40.0)
        amt2 = LinkedListNode(60.5)
        record1 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt1, 'ZIP_CODE': None,
                   'TRANSACTION_DT': date}
        record2 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt2, 'ZIP_CODE': None,
                   'TRANSACTION_DT': date}

        id = InfoIndividual(record1)
        id.update_by_date(record2)
        info_date = id.get_date_dict_entry(date)

        self.assertEqual(info_date.get_median(), 50)
        self.assertEqual(info_date.get_count(), 2)
        self.assertAlmostEqual(info_date.get_total(), 100.5)

    def test_different_date_update(self):
        id = 'C00629618'
        date1 = '01022017'
        date2 = '10212000'
        amt1 = LinkedListNode(40.0)
        amt2 = LinkedListNode(60.5)
        record1 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt1, 'ZIP_CODE': None,
                   'TRANSACTION_DT': date1}
        record2 = {'CMTE_ID': id, 'TRANSACTION_AMT': amt2, 'ZIP_CODE': None,
                   'TRANSACTION_DT': date2}

        id = InfoIndividual(record1)
        id.update_by_date(record2)
        info_date1 = id.get_date_dict_entry(date1)
        info_date2 = id.get_date_dict_entry(date2)

        self.assertEqual(info_date1.get_median(), 40)
        self.assertEqual(info_date1.get_count(), 1)
        self.assertAlmostEqual(info_date1.get_total(), 40)

        self.assertEqual(info_date2.get_median(), 61)
        self.assertEqual(info_date2.get_count(), 1)
        self.assertAlmostEqual(info_date2.get_total(), 60.5)
