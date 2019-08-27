from django.test import TestCase
from cohort_manager.models import AssignmentImport
from io import StringIO
from datetime import datetime
import csv


class AssignmentImportTest(TestCase):
    def to_csv(self, rows=[]):
        s = StringIO()

        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(AssignmentImport.FIELD_NAMES)
        for row in rows:
            writer.writerow(row)

        csv_data = s.getvalue()
        s.close()
        return csv_data

    def test_json_data(self):
        import1 = AssignmentImport(
            comment='comment', is_file_upload=False, created_by='javerage')
        import1.save()

        data = import1.json_data()
        self.assertIsNotNone(data['id'])
        self.assertEqual(data['comment'], 'comment')
        self.assertEqual(data['is_file_upload'], False)
        self.assertIsNotNone(data['created_date'])
        self.assertEqual(data['created_by'], 'javerage')
        self.assertEqual(data['imported_date'], None)
        self.assertEqual(data['imported_status'], None)
        self.assertEqual(data['imported_message'], None)
        self.assertEqual(data['assignments'], [])
        self.assertEqual(data['errors'], [])

        # With assignments
        import1.document = self.to_csv([[1234567, 0, 2019, 4, 1, 123],
                                        [1234568, 0, 2019, 4, 1, None]])
        data = import1.json_data()
        self.assertEqual(len(data['assignments']), 2)
        self.assertEqual(len(data['errors']), 1)

        # Imported
        import1.imported_date = datetime(2015, 10, 10)
        import1.imported_status = 200
        import1.imported_message = 'Success'

        data = import1.json_data()
        self.assertEqual(data['imported_date'], '2015-10-10T00:00:00')
        self.assertEqual(data['imported_status'], 200)
        self.assertEqual(data['imported_message'], 'Success')

    def test_assignment_errors(self):
        imp = AssignmentImport()
        a, errors = imp.assignments()
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        imp.document = None
        a, errors = imp.assignments()
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        imp.document = self.to_csv()
        a, errors = imp.assignments()
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        imp.document = self.to_csv([[1234567, 0, 2019, 4, 1, 123],
                                    [1234568, 0, 2019, 4, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 0)

        imp.document = self.to_csv([[1234567, 0, 2019, 4, 1, None],
                                    [1234568, 0, 2019, 4, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 1)

        imp.document = self.to_csv([[1234567, 0, None, 4, 1, 123],
                                    [1234568, 0, 2019, None, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 2)

        imp.document = b'<html>'
        self.assertRaises(TypeError, imp.assignments)
