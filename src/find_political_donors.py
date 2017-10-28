import argparse
from FECDate import *
from Info import infoIndividual
from lib import *
from linkedListNode import linkedListNode
from BSTree import BSTree, nodeID


def stream_input(filename):
    """
    Stream input file line by line
    Yield valid data lines
    
    :param filename: string, path to the file
    
    :return: extracted_info: dictionary generator,
        extracted information required for further processing
             
    """
    try:
        file = open(filename, 'r')

        # Iterate the file till the end of the file
        while True:
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
            extracted_info = dict(\
                zip(INFO_HEADER, \
                    [entries[j] for j in [INPUT_HEADER[i] for i in INFO_HEADER]]))

            print extracted_info

            # Validate extracted information
            # Validate the format of CMTE_ID
            if not extracted_info['CMTE_ID'][0] is 'C' or \
                    not extracted_info['CMTE_ID'][1:].isdigit() or \
                    len(extracted_info['CMTE_ID']) != 9:
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

        file.close()

    except IOError:
        print("File not found")


def update_info_database(line):
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
    # TODO: allow default input and output path
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path to input file")
    parser.add_argument("output_by_zip", type=str, help=\
        "path to output: medianvals_by_zip" )
    parser.add_argument("output_by_date", type=str, help=\
        "path to output: medianvals_by_date" )
    args = parser.parse_args()

    filein_path = args.input
    fileout_zip = open(args.ouput_by_zip, 'wa')
    fileout_date = open(args.output_by_date, 'w')

    # information database that saves all the donation data
    # structure:
    # {id: object infoIndividual}
    infoDB = dict()

    # self-balancing binary search tree that saves
    # the recipient and transaction date in order
    infoBSTree = BSTree()

    # iterate through each line of input files
    for line in stream_input(filein_path):

        # update information database from the line streamed in
        # obtain the recipient information
        info = update_info_database(line)

        # If the info contains zip code information:
        # add the updated entry (donation to recipient id from area zip_code)
        # to medianvals_by_zip file
        if line['ZIP_CODE']:
            # Currently, the output method only checks whether
            # the zip code is already in the database
            # TODO: check whether the [id][zip_code] entry is just updated (by flag?)
            fileout_zip.write(info.output_by_zip(line['ZIP_CODE']))

        # if the info contains transaction date information:
        # add to transaction date output file
        if line['TRANSACTION_DT']:
            # construct new infoBSTree node from information in infoDB
            new_node = nodeID(info.get_id(), info.get_date(),
                              info.get_date_dict_entry[line['TRANSACTION_DT']])
            infoBSTree.update(new_node)
            fileout_date.writelines(infoBSTree.output_tree_inorder())

    fileout_zip.close()
    fileout_date.close()
