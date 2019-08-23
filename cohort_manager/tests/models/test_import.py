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

    def test_validate(self):
        data = [[1234567, 0, 2019, 4, 1, 123],
                [1234568, 0, 2019, 4, 1, 124]]
        imp = AssignmentImport(
            status_code='200', document=self._csv(data), imported_by='j')
        imp.validate()
        self.assertEqual(len(imp.assignment_errors), 0)

        data = [[1234567, 0, 2019, 4, 1, None],
                [1234568, 0, 2019, 4, 1, 124]]
        imp = AssignmentImport(
            status_code='200', document=self._csv(data), imported_by='j')
        imp.validate()
        self.assertEqual(len(imp.assignment_errors), 1)

        data = [[1234567, 0, None, 4, 1, 123],
                [1234568, 0, 2019, None, 1, 124]]
        imp = AssignmentImport(
            status_code='200', document=self._csv(data), imported_by='j')
        imp.validate()
        self.assertEqual(len(imp.assignment_errors), 2)
        print(imp.assignment_errors)
