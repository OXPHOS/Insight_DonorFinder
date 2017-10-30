import datetime
import sys

INPUT_HEADER = {
    'CMTE_ID':0,
    'ZIP_CODE':10,
    'TRANSACTION_DT':13,
    'TRANSACTION_AMT':14,
    'OTHER_ID':15
} # Column index of important fields of records downloaded from FEC websoites

INFO_HEADER = ['CMTE_ID', 'TRANSACTION_AMT', 'ZIP_CODE', 'TRANSACTION_DT']

COLSIZE = 21 # Total fields of records downloaded from FEC website


def stream_input(filename):
    """
    Stream input file line by line
    Yield valid data lines

    :param filename: string, path to the file

    :return: extracted_info: dictionary generator,
        extracted information required for further processing

    """
    file = open(filename, 'r')

    # for progress bar
    counter = 0
    sys.stdout.write('PROGRESS(every 1000 reads): \n')
    sys.stdout.write('.')
    sys.stdout.flush()

    # Iterate the file till the end of the file
    while True:
        counter += 1
        if counter == 1000:
            sys.stdout.write('.')
            sys.stdout.flush()
            counter = 0

        line = file.readline()
        if line in ['\n', '', ' ']:
            break

        entries = line.split('|')

        # Integrity check
        if len(entries) != COLSIZE:
            continue
        # Input file considerations rule 5:
        # Remove entries with empty CMTE_ID or TRANSACTION_AMT
        elif (not entries[INPUT_HEADER['CMTE_ID']]) or \
                (not entries[INPUT_HEADER['TRANSACTION_AMT']]):
            continue
        # Input file consideration rule 1:
        # Remove entries with contributors from entities
        elif entries[INPUT_HEADER['OTHER_ID']]:
            continue

        # Extract CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        extracted_info = dict( \
            zip(INFO_HEADER, \
                [entries[j] for j in [INPUT_HEADER[i] for i in INFO_HEADER]]))

        # Validate extracted information
        # Validate the format of CMTE_ID
        if not extracted_info['CMTE_ID'][0] is 'C' or \
            not extracted_info['CMTE_ID'][1:].isdigit() or \
                len(extracted_info['CMTE_ID']) != 9:
            continue

        # Validate that the transaction amount
        try:
            extracted_info['TRANSACTION_AMT'] = \
                float(extracted_info['TRANSACTION_AMT'])
            # corner case: transaction amount = 0.0
            if not extracted_info['TRANSACTION_AMT']:
                continue
        except ValueError:
            continue

        # Validate zip code
        # Input file consideration rule 3, 4
        # Based on FEC rules, zip code has to be 9 digits
        if not extracted_info['ZIP_CODE'].isdigit() or \
                len(extracted_info['ZIP_CODE']) != 9:
            extracted_info['ZIP_CODE'] = None
        else:
            extracted_info['ZIP_CODE'] = extracted_info['ZIP_CODE'][0:5]

        # Validate transaction date
        if not validate_date(extracted_info['TRANSACTION_DT']):
            extracted_info['TRANSACTION_DT'] = None

        # If both zip code and transaction date information are missing:
        # Skip the entry
        if (not extracted_info['TRANSACTION_DT']) and \
                (not extracted_info['ZIP_CODE']):
            continue

        yield extracted_info
        # TODO: According to FEC Metadata Description:
        # Col21 is required, Col7 specifies entity type (IND, etc.)
        # These two criteria can also be taken into consideration

    file.close()


def validate_date(date):
    """
    Validate if the date strain is a real date via built-in datetime.date type
    :param date: string, FEC style date
    :return: boolean, return True if the date string can be converted to a real date
    """
    if not isinstance(date, str) or len(date) != 8 or (not date.isdigit()):
        return False

    try:
        if datetime.date(*map(int, [date[-4:], date[0:2], date[2:4]])):
            return True
    except ValueError:
        return
