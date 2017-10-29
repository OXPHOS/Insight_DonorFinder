import datetime


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
