from django.test import TestCase
from django.core.exceptions import ValidationError
from cohort_manager.models import AssignmentImport
from io import StringIO
import csv


class AssignmentImportTest(TestCase):
    header = ['system_key', 'campus', 'app_year', 'app_quarter', 'app_number',
              'AdmissionSelectionID']

    def _csv(self, rows=[]):
        s = StringIO()

        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(self.header)
        for row in rows:
            writer.writerow(row)

        csv_data = s.getvalue()
        s.close()
        return csv_data

    def test_assignment_errors(self):
        a, errors = AssignmentImport().assignments
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        a, errors = AssignmentImport(document=None).assignments
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        a, errors = AssignmentImport(document='<html>').assignments
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        a, errors = AssignmentImport(document=self._csv()).assignments
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        data = [[1234567, 0, 2019, 4, 1, 123],
                [1234568, 0, 2019, 4, 1, 124]]
        a, errors = AssignmentImport(document=self._csv(data)).assignments
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 0)

        data = [[1234567, 0, 2019, 4, 1, None],
                [1234568, 0, 2019, 4, 1, 124]]
        a, errors = AssignmentImport(document=self._csv(data)).assignments
        self.assertEqual(len(a), 1)
        self.assertEqual(len(errors), 1)

        data = [[1234567, 0, None, 4, 1, 123],
                [1234568, 0, 2019, None, 1, 124]]
        a, errors = AssignmentImport(document=self._csv(data)).assignments
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 2)
