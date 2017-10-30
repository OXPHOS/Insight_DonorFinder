from LinkedListNode import *


class InfoByDomainBase(object):
    """
    Base class for median information storage

    The class has the following member variables:
        - self._count: the count of donation to specific recipient
            with specific grouping rules ,
        - self._median: round median of donation to specific recipient 
            with specific grouping rules,
        - self._total : total donations to to specific recipient 
            with specific grouping rules,
        - self._median_left, self._median_right: objects of the doubly 
            linked list, as indexes for median position

    :param amount: float, the amount of current transaction

    """

    def __init__(self, amount):
        if not amount:
            self._median = 0
            self._count = 0
            self._total = 0
            self._median_left = None
            self._median_right = None
        else:
            self._median = int(round(amount))
            self._count = 1
            self._total = amount
            self._median_left = LinkedListNode(amount)
            self._median_right = self._median_left

    def get_median(self):
        return self._median

    def get_count(self):
        return self._count

    def get_total(self):
        return self._total

    def get_median_left(self):
        return self._median_left

    def get_median_right(self):
        return self._median_right

    def update(self, amount):
        """
        Update member variables based on new amount coming in

        :param new_amountLLN: float, the amount of current transaction

        """
        new_amountLLN = LinkedListNode(amount)

        # Corner case: initiated empty InfoByDomain class
        if (not self._median_left) or (not self._median_right):
            self._median = int(round(new_amountLLN.get_value()))
            self._count = 1
            self._total = new_amountLLN.get_value()
            self._median_left = LinkedListNode(new_amountLLN.get_value())
            self._median_right = self._median_left
            return

        # insert new donation amount to the doubly linked list
        # update median position information
        if new_amountLLN.get_value() > self._median:
            LinkedListNode.insert_linkedlist_node(self._median_right, new_amountLLN, 'r')
            if new_amountLLN.get_value() > self._median_right.get_value():
                # if odd numbers of donation present in the linked list before new node joining:
                # Shift the median set by 1
                if self._median_left is self._median_right:
                    self._median_left, self._median_right = \
                        self._median_right, self._median_right.right
                # if even number of donation present in the linked list before new node joining:
                # Overlap self._median_left and self._median_right
                else:
                    self._median_left, self._median_right = self._median_right, self._median_right
            else:
                # Must be even number of donation present in the linked list before new node joining
                self._median_left, self._median_right = new_amountLLN, new_amountLLN

        else:
            LinkedListNode.insert_linkedlist_node(self._median_left, new_amountLLN, 'l')
            if new_amountLLN.get_value() <= self._median_left.get_value():
                # if odd numbers of donation present in the linked list before new node joining:
                # Shift the median set by 1
                if self._median_left is self._median_right:
                    self._median_left, self._median_right = \
                        self._median_left.left, self._median_left
                # if even number of donation present in the linked list before new node joining:
                # Overlap self._median_left and self._median_right
                else:
                    self._median_left, self._median_right = self._median_left, self._median_left
            else:
                self._median_left, self._median_right = new_amountLLN, new_amountLLN

        # update count, median and total information
        self._count += 1
        self._median = int(round(float(self._median_left.get_value() + \
                                  self._median_right.get_value()) / 2))
        self._total += new_amountLLN.get_value()

    def output(self):
        """
        Only convert the total to int during output
        :return: median|count|total
        """
        return '|'.join(map(str, [self._median, self._count,
                                  int(round(self._total))])) + '\n'

    def __repr__(self):
        return "InfoByDomainBase: " + ','.join(map(str, [
            self._median, self._count, self._total,
            self._median_left, self._median_right]))


class InfoByZip(InfoByDomainBase):
    """
    Derived from infoByDomainBase
    Saves the donation information to specific recipient
    which is grouped by zip code
    """

    def __repr__(self):
        return "Group by zips: " + ','.join(map(str, [
            self._median, self._count, self._total,
            self._median_left, self._median_right]))


class InfoByDate(InfoByDomainBase):
    """
    Derived from infoByDomainBase
    Saves the donation information to specific recipient
    which is grouped by transaction date
    """

    def __repr__(self):
        return "Group by dates: " + ','.join(map(str, [
            self._median, self._count, self._total,
            self._median_left, self._median_right]))


class InfoIndividual(object):
    """
    structure saves all donation information of a specific recipient,
    with information:
        - self._id: id of the recipient
        - self._zip: zip code of the donation source (None/zip code)
        - self._date: transaction date (None/date)
        - self._zip_dict: {zip code: object infoByZip}
        - self._date_dict: {transaction date: object infoByDate}

    :param line: dictionary of CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT

    """

    def __init__(self, line):
        self._id = line['CMTE_ID']
        self._zip_dict = dict()
        self._date_dict = dict()

        try:
            if line['ZIP_CODE']:
                self._zip_dict[line['ZIP_CODE']] = InfoByZip(line['TRANSACTION_AMT'])
            if line['TRANSACTION_DT']:
                self._date_dict[line['TRANSACTION_DT']] = InfoByDate(line['TRANSACTION_AMT'])
        except KeyError:
            pass

    def has_zip(self, zipcode):
        """
        whether the area with input zip code has donated to the recipient before
        :param zipcode: zip code
        :return: boolean
            True: the area with input zip code has donated to the recipient before
            False: the area with input zip code hasn't donated to the recipient before
        """
        return zipcode in self._zip_dict

    def has_date(self, date):
        """
        whether there is donation record on the input date to the recipient before
        :param date: transaction date
        :return: boolean
            True: There is donation record on the input date to the recipient before
            False: There isn't donation record on the input date to the recipient before
        """
        return date in self._date_dict

    def get_id(self):
        """
        :return: string, id of recipient (CMTE_ID) 
        """
        return self._id

    def get_zip_dict_entry(self, key):
        """
        return median, total and count information to specific recipient at specific area
        :param key: string, zip code
        :return: object infoByZip or None
        """
        try:
            return self._zip_dict[key]
        except KeyError:
            return None

    def get_date_dict_entry(self, key):
        """
        return median, total and count information to specific recipient on specific day
        :param key: string, transaction date
        :return: object infoByDate or None
        """
        try:
            return self._date_dict[key]
        except KeyError:
            return None

    def update_by_zip(self, line):
        """
        Update donation information to specific recipient based on zip code
        Create the zip-infoByZip key-value pair if the zip code shows up 
        for the first time

        :param line: dictionary of CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        """
        if self.has_zip(line['ZIP_CODE']):
            self._zip_dict[line['ZIP_CODE']].update(line['TRANSACTION_AMT'])
        else:
            self._zip_dict[line['ZIP_CODE']] = InfoByZip(line['TRANSACTION_AMT'])

    def update_by_date(self, line):
        """
        Update donation information to specific recipient based on zip code
        Create the date-infoByDate key-value pair if the transaction date 
        shows up for the first time

        :param line: dictionary of CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        """
        if self.has_date(line['TRANSACTION_DT']):
            self._date_dict[line['TRANSACTION_DT']].update(line['TRANSACTION_AMT'])
        else:
            self._date_dict[line['TRANSACTION_DT']] = InfoByDate(line['TRANSACTION_AMT'])

    def update_info(self, line):
        """
        wrapper method of donation information update

        :param line: dictionary of CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        """
        if line['ZIP_CODE']:
            self.update_by_zip(line)
        if line['TRANSACTION_DT']:
            self.update_by_date(line)

    def output_by_zip(self, zipcode):
        """
        Output donation information to specific recipient from specific zip code
        return empty string if the entry is missing

        Currently, the output method only checks whether 
        the zip code is already in the database
        TODO: check whether the [id][zip_code] entry is just updated (by flag?)

        :param zipcode: int, zip code entry to be output
        :return: string with format CMTE_ID|ZIP_CODE|MEDIAN|COUNT|TOTAL

        """
        if self.has_zip(zipcode):
            return self._id + '|' + zipcode + '|' + \
                   self._zip_dict[zipcode].output()
        else:
            return ''

    def output_by_date(self, date):
        """
        Output donation information to specific recipient on specific date
        return empty string if the entry is missing

        :param date: int, zip code entry to be output
        :return: string with format CMTE_ID|ZIP_CODE|MEDIAN|COUNT|TOTAL

        """
        if self.has_date(date):
            return self._id + '|' + date + '|' + \
                   self._date_dict[date].output_NodeByDate()
        else:
            return ''

    def __repr__(self):
        return self._id + ': ' + str(self._zip_dict) + '; ' + str(self._date_dict)
