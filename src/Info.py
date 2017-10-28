from linkedListNode import *

class infoByDomainBase(object):
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
     
    :param amountLLN: linkedListNode object wrapping the amount
        of current transaction
    
    """
    def __init__(self, amountLLN):
        self._median = int(round(amountLLN.val))
        self._count = 1
        self._total = amountLLN.val
        self._median_left = amountLLN
        self._median_right = amountLLN

    def update(self, new_amountLLN):
        """
        Update member variables based on new amount coming in
        
        :param new_amountLLN: linkedListNode object wrapping the amount
            of current transaction

        """
        # insert new donation amount to the doubly linked list
        # update median position information
        if new_amountLLN.val > self._median:
            linkedListNode.insert_linkedlist_node(self._median_right, new_amountLLN, 'r')

            # if odd numbers of donation present in the doubly linked list:
            # Shift the median set by 1
            if self._median_left is self._median_right:
                self._median_left, self._median_right = (self._median_right, new_amountLLN)
            elif new_amountLLN.val > self._median_right.val:
                self._median_left, self._median_right = (self._median_right, self._median_right)
            else:
                self._median_left, self._median_right = (new_amountLLN, new_amountLLN)
        else:
            linkedListNode.insert_linkedlist_node(self._median_left, new_amountLLN, 'l')
            if self._median_left is self._median_right:
                self._median_left, self._median_right = (new_amountLLN, self._median_left)
            elif new_amountLLN.val < self._median_left.val:
                self._median_left, self._median_right = (self._median_left, self._median_left)
            else:
                self._median_left, self._median_right = (new_amountLLN, new_amountLLN)

        # update count, median and total information
        self._count += 1
        self._median = int(round(self._median_left.val + \
                                 self._median_right.val) / 2)
        self._total = new_amountLLN.val

    def output(self):
        """
        :return: median|count|total
        """
        return '|'.join(map(str, [self.median, self.count, self.total]))+'\n'


class infoByZip(infoByDomainBase):
    """
    Derived from infoByDomainBase
    Saves the donation information to specific recipient
    which is grouped by zip code
    """
    def __repr__(self):
        return "Group by zips: " + ','.join(map(str, [
                self.median, self.count, self.median_set]))


class infoByDate(infoByDomainBase):
    """
    Derived from infoByDomainBase
    Saves the donation information to specific recipient
    which is grouped by transaction date
    """
    def __repr__(self):
        return "Group by dates: " + ','.join(map(str, [
                self.median, self.count, self.median_set]))


class infoIndividual(object):
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
        self._zip = line['ZIP_CODE']
        self._date = line['TRANSACTION_DT']
        self._zip_dict = dict()
        self._date_dict = dict()

        if self._zip:
            self._zip_dict[self._zip] = infoByZip(line['TRANSACTION_AMT'])
        if self._date:
            self._date_dict[self._date] = infoByDate(line['TRANSACTION_AMT'])

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

    def get_date(self):
        """
        :return: object FECDate, transaction date (TRANSACTION_DT) 
        """
        return self._date

    def get_date_dict_entry(self, key):
        """
        return median, total and count information to specific recipient on specific day
        :param key: object FECDate, transaction date
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
            self._zip_dict[self._zip].update(line['TRANSACTION_AMT'])
        else:
            self._zip_dict[self._zip] = infoByZip(line['TRANSACTION_AMT'])

    def update_by_date(self, line):
        """
        Update donation information to specific recipient based on zip code
        Create the date-infoByDate key-value pair if the transaction date 
        shows up for the first time

        :param line: dictionary of CMTE_ID, TRANSACTION_AMT, ZIP_CODE and TRANSACTION_DT
        """
        if self.has_date(line['TRANSACTION_DT']):
            self._date_dict[self._date].update(line['TRANSACTION_AMT'])
        else:
            self._date_dict[self._date] = infoByZip(line['TRANSACTION_AMT'])

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
            return self._id + '|' + str(self._zip) + '|' + \
                   self._zip_dict[self._zip].output()
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
            return self._id + '|' + str(self._date) + '|' + \
                   self._date_dict[self._date].output()
        else:
            return ''