import argparse
from FECDate import *
from Info import infoIndividual
from lib import *
from linkedListNode import linkedListNode
from BSTree import BSTree, nodeID

def _stream_input(filename):
    """
    Stream input file line by line
    Yield valid data lines
    
    :param filename: string, path to the file
    
    :return: extracted_info: dictionary generator,
        extracted information required for further processing
             
    """
    try:
        file = open(INPUT_PATH+filename, 'rb')

        # Iterate the file till the end of the file
        while True:
            line = file.readline()
            if line == '\n' or '':
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
            extracted_info = dict(\
                zip(INFO_HEADER, \
                    [entries[j] for j in [INPUT_HEADER[i] for i in INFO_HEADER]]))

            print extracted_info

            # Validate extracted information
            # Validate the format of CMTE_ID
            if not extracted_info['CMTE_ID'][0] is 'C' or \
                    not extracted_info['CMTE_ID'][1:].isdigit():
                continue

            # Validate that the transaction amount
            try:
                extracted_info['TRANSACTION_AMT'] = \
                    linkedListNode(float(extracted_info['TRANSACTION_AMT']))
            except SyntaxError:
                continue

            # Validate zip code
            # Input file consideration rule 3, 4
            if not extracted_info['ZIP_CODE'].isdigit() or \
                            len(extracted_info['ZIP_CODE']) < 5:
                extracted_info['ZIP_CODE'] = None
            else:
                extracted_info['ZIP_CODE'] = int(extracted_info['ZIP_CODE'][0:5])

            # Validate transaction date via FECDate class
            try:
                extracted_info['TRANSACTION_DT'] = FECDate(extracted_info['TRANSACTION_DT'])
            except TypeError:
                extracted_info['TRANSACTION_DT'] = None

            yield extracted_info

    except IOError:
        print("File not found")


def _update_info_database(line):
    """
    Take the line streamed in, update information database with key: 
    id of the recipient of current donation
    
    update both donation_by_zip and donation_by_date information to the recipient 
    when possible.
    
    :param line: dict, input line with fields: 
        CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        
    :return: object infoIndividual, contains the summary of the donation the recipient
        has received so far.
    """
    id = line['CMTE_ID']

    if id in infoDB:
        infoDB[id].update_info(line)
    else:
        infoDB[id] = infoIndividual(line)

    return infoDB[id]

if __name__ == "__main__":

    # Argument parser
    # If no arg: read all files from ../input
    # else: input file number and file name. The files must be in ../input folder
    parser = argparse.ArgumentParser()
    #inputnumber
    inputs = '../input/donor_dataset_1' # Please put files in /inputs and only specify filename here

    # information database that saves all the donation data
    # structure:
    # {id: object infoIndividual}
    infoDB = dict()

    # self-balancing binary search tree that saves
    # the recipient and transaction date in order
    infoBSTree = BSTree()

    # TODO: f.open(): open output files // at least open zips file

    # iterate through the files
    for filename in inputs:

        # iterate through each line of input files
        for line in _stream_input(filename):

            # update information database from the line streamed in
            # obtain the recipient information
            info = _update_info_database(line)

            # If the info contains zip code information:
            # add the updated entry (donation to recipient id from area zip_code)
            # to medianvals_by_zip file
            if line['ZIP_CODE']:
                # Currently, the output method only checks whether
                # the zip code is already in the database
                # TODO: check whether the [id][zip_code] entry is just updated (by flag?)
                info.output_by_zip(line['ZIP_CODE'])

            # if the info contains transaction date information:
            # add to transaction date output file
            if line['TRANSACTION_DT']:
                # construct new infoBSTree node from information in infoDB
                new_node = nodeID(info.get_id(), info.get_date(),
                                  info.get_date_dict_entry[line['TRANSACTION_DT']])
                infoBSTree.update(new_node)
                infoBSTree.output_tree_inorder()

    # TODO: f.close()








