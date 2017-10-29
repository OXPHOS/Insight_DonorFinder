#!/usr/bin/env python

from src.LinkedListNode import *
from src.validate_date import *
from src.InfoTable import *
from src.AVLTree import *
from src.find_political_donors import *

INPUT_HEADER = {
    'CMTE_ID':0,
    'ZIP_CODE':10,
    'TRANSACTION_DT':13,
    'TRANSACTION_AMT':14,
    'OTHER_ID':15
} # Column index of important fields of records downloaded from FEC websoites

INFO_HEADER = ['CMTE_ID', 'TRANSACTION_AMT', 'ZIP_CODE', 'TRANSACTION_DT']

COLSIZE = 21 # Total fields of records downloaded from FEC website
