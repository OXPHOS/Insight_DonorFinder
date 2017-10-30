import argparse
from src import *


def update_info_database(line):
    """
    Take the line streamed in, update information database with key: 
    id of the recipient of current donation

    update both donation_by_zip and donation_by_date information to the recipient 
    when possible.

    :param line: dict, input line with fields: 
        CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT

    :return: object infoIndividual, contains the summary of the donation 
        the recipient has received so far.
    """
    id = line['CMTE_ID']

    if id in infoDB:
        infoDB[id].update_info(line)
    else:
        infoDB[id] = InfoIndividual(line)

    return infoDB[id]


if __name__ == "__main__":
    # Argument parser
    # TODO: allow default input and output path
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path to input file")
    parser.add_argument("output_by_zip", type=str, help= \
                        "path to output: medianvals_by_zip")
    parser.add_argument("output_by_date", type=str, help= \
                        "path to output: medianvals_by_date")
    args = parser.parse_args()

    # information database that saves all the donation data
    # structure:
    # {id: object infoIndividual}
    infoDB = dict()

    # self-balancing binary search tree that saves
    # the recipient and transaction date in order
    infoAVLTree = AVLTreeByID()

    try:
        # open medianvals_by_zip file since it requires streaming
        fileout_zip = open(args.output_by_zip, 'w')

        # iterate through each line of input files
        for line in stream_input(args.input):

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
                # construct new infoAVLTree node from information in infoDB
                new_node = NodeByID(info.get_id(), line['TRANSACTION_DT'],
                                    info.get_date_dict_entry(line['TRANSACTION_DT']))
                infoAVLTree.update_tree(new_node)

                # Write the updated tree to output via in-order traversal
                fileout_date = open(args.output_by_date, 'w')
                for entry in infoAVLTree.output():
                    fileout_date.write(entry)
                fileout_date.close()

        # close medianvals_by_zip file
        fileout_zip.close()

    except IOError:
        print("Invalid file or file path.")
