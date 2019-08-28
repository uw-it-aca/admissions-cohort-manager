from io import StringIO
import csv


def to_csv(data=[]):
    """
    Return a CSV-formatted string containing the items in the passed list.
    """
    s = StringIO()

    csv.register_dialect('unix_newline', lineterminator='\n')
    csv.writer(s, dialect='unix_newline').writerow(data)

    csv_data = s.getvalue()
    s.close()
    return csv_data
