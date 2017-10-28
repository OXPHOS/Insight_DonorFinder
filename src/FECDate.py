import datetime

class FECDate(object):
    """
    The class wraps around python datetime module
    and keeps the date in FEC style for the convenience of output
    
    The date that cannot be converted to python datetime type 
    will throw TypeError
    
    :param date: string, date in FEC style
    """
    def __init__(self, date):
        self.date = self.isFECDate(self, date)
        if not self.date:
            raise TypeError ("Invalid date type")
        else:
            self._date_str = date

    def isFECDate(self, date):
        """
        Check if the input date string is a valid date
        
        :param date: string, date in FEC style
        :return: object datetime.datetime
        """
        if not isinstance(date, str) or len(date) != 8 or (not date.isdigit()): ## Note: unicode??
            return None

        try:
            return datetime.datetime(map(int, [date[-4:], date[2:4], date[0:2]]))
        except ValueError:
            return None

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return self.date != other.date

    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.key_idx

    def __lt__(self, other):
        return not self.date <= other.date

    def __le__(self, other):
        return not self.date <= other.date

    def __repr__(self):
        return self._date_str
