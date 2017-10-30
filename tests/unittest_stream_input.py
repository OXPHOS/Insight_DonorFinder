import unittest
import tempfile
from src import stream_input
from src import LinkedListNode


class TestInputParser(unittest.TestCase):
    def test_column_check(self):
        # Valid entry requires 21 columns (empty ones counted)
        fd = tempfile.NamedTemporaryFile(delete=False)
        fd.write('C00629618||||||IND||||900170235|||01032017|40')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(0, len(res))

    def test_id_and_amount_check(self):
        # Input file considerations rule 5:
        # Remove entries with empty CMTE_ID or TRANSACTION_AMT
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Missing ID
        fd.write('||||||IND||||900170235|||01032017|40||||||'+'\n')
        # Missing amount value
        fd.write('C00629618||||||IND||||900170235|||01032017|||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(0, len(res))

    def test_other_id_check(self):
        # Input file consideration rule 1:
        # Remove entries with contributors from entities
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Other_ID = 'NOT_INDIVIDUAL'
        fd.write('C00629618||||||IND||||900170235|||01032017|40|NOT_INDIVIDUAL|||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(0, len(res))

    def test_id_validation_check(self):
        # ID format: C123456789
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Missing 'C'
        fd.write('00629618||||||IND||||900170235|||01032017|40||||||'+'\n')
        # Incomplete digits
        fd.write('C0062968||||||IND||||900170235|||01032017|40||||||'+'\n')
        # Multiple letters
        fd.write('C0062961F||||||IND||||900170235|||01032017|40||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(0, len(res))

    def test_amount_validation_check(self):
        # Input file considerations rule 5:
        # Remove entries with empty CMTE_ID or TRANSACTION_AMT
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Amount unable to be converted to number
        fd.write('C00629618||||||IND||||900170235|||01032017|40C||||||'+'\n')
        # Amount equals zero
        fd.write('C00629618||||||IND||||900170235|||01032017|0||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(0, len(res))

        # Check the instance of amount (LinkedListNode) from valid entry
        fd = tempfile.NamedTemporaryFile(delete=False)
        fd.write('C00629618||||||IND||||900170235|||01032017|40||||||' + '\n')
        fd.close()
        for line in stream_input(fd.name):
            res = line
        self.assertIsInstance(res['TRANSACTION_AMT'], LinkedListNode)

    def test_zip_code(self):
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Missing zip code
        fd.write('C00629618||||||IND|||||||01032017|40||||||'+'\n')
        # Less or equal than 5 digits
        fd.write('C00629618||||||IND||||90017|||01032017|40||||||'+'\n')
        # Has invalid symbol
        fd.write('C00629618||||||IND||||90017023B|||01032017|40||||||'+'\n')
        # Valid zip code
        fd.write('C00629618||||||IND||||900170235|||01032017|40||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        size = 4
        ref = [{} for _ in xrange(size)]
        ref[0] = {'ZIP_CODE': None}
        ref[1] = {'ZIP_CODE': None}
        ref[2] = {'ZIP_CODE': None}
        ref[3] = {'ZIP_CODE': '90017'}

        self.assertEqual(size, len(res))
        for i in xrange(size):
            self.assertEqual(ref[i]['ZIP_CODE'], res[i]['ZIP_CODE'])

    def test_transaction_date(self):
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Invalid date
        fd.write('C00629618||||||IND||||900170235|||02312017|40||||||'+'\n')
        # Incomplete date
        fd.write('C00629618||||||IND||||900170235|||2017|40||||||'+'\n')
        # Valid date
        fd.write('C00629618||||||IND||||900170235|||01032017|40||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        size = 3
        ref = [{} for _ in xrange(size)]
        ref[0] = {'TRANSACTION_DT': None}
        ref[1] = {'TRANSACTION_DT': None}
        ref[2] = {'TRANSACTION_DT': '01032017'}

        self.assertEqual(size, len(res))
        for i in xrange(size):
            self.assertEqual(ref[i]['TRANSACTION_DT'], res[i]['TRANSACTION_DT'])

    def test_acceptable_complete_entry(self):
        fd = tempfile.NamedTemporaryFile(delete=False)
        # Complete entry
        fd.write('C00629618||||||IND||||900170235|||01032017|40||||||'+'\n')
        # Skip entries with neither zip code nor transaction date
        fd.write('C00384818||||||IND||||||||333||||||'+'\n')
        fd.close()

        res = []
        for line in stream_input(fd.name):
            res.append(line)

        self.assertEqual(1, len(res))
        ref = {'CMTE_ID': 'C00629618', 'TRANSACTION_AMT': 40.0, 'ZIP_CODE': '90017',
               'TRANSACTION_DT': '01032017'}
        self.assertEqual(ref['CMTE_ID'], res[0]['CMTE_ID'])
        self.assertEqual(ref['TRANSACTION_AMT'], res[0]['TRANSACTION_AMT'].get_value())
        self.assertEqual(ref['ZIP_CODE'], res[0]['ZIP_CODE'])
        self.assertEqual(ref['TRANSACTION_DT'], res[0]['TRANSACTION_DT'])
