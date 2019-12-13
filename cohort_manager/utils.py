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


def dict_to_csv(data, fieldnames):
    """
    Return a CSV-formatted string containing the items in the dict.
    """
    s = StringIO()

    csv.register_dialect('unix_newline', lineterminator='\n', delimiter='\t')
    writer = csv.DictWriter(s,
                            dialect='unix_newline',
                            fieldnames=fieldnames)

    writer.writerow(data)

    csv_data = s.getvalue()
    s.close()
    return csv_data


def get_headers(fieldnames):
    """"
    Return a CSV-formatted headers for the given fieldnames
    """
    s = StringIO()

    csv.register_dialect('unix_newline', lineterminator='\n', delimiter='\t')
    writer = csv.DictWriter(s,
                            dialect='unix_newline',
                            fieldnames=fieldnames)

    writer.writeheader()

    csv_data = s.getvalue()
    s.close()
    return csv_data
