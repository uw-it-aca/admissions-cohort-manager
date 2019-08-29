from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from cohort_manager.models import AssignmentImport, Assignment
from cohort_manager.utils import to_csv
from datetime import datetime
from io import StringIO


class AssignmentTest(TestCase):
    def setUp(self):
        self.assignment = Assignment(
                system_key='1',
                campus='0',
                year=2020,
                quarter=3,
                application_number='8',
                admission_selection_id='000',
                cohort='65')

    def test_json_data(self):
        self.assertEqual(self.assignment.json_data(), {
            'admission_selection_id': '000',
            'application_number': '8',
            'campus': '0',
            'cohort': '65',
            'major': '',
            'quarter': 3,
            'system_key': '1',
            'year': 2020})

    def test_csv_data(self):
        self.assertEqual(self.assignment.csv_data(), '1,0,2020,3,8,000\n')


class AssignmentImportTest(TestCase):
    def _csv(self, rows=[]):
        csv_data = to_csv(AssignmentImport.FIELD_NAMES)
        for row in rows:
            csv_data += to_csv(row)
        return csv_data

    def test_create_from_file(self):
        file_data = self._csv([[1234567, 0, 2019, 4, 1, 123],
                               [1234568, 0, 2019, 4, 1, 124]])

        uploaded_file = SimpleUploadedFile(
            'test.csv', file_data.encode(), content_type='text/csv')

        imp = AssignmentImport.objects.create_from_file(
            uploaded_file=uploaded_file, created_by='javerage')
        self.assertEqual(imp.is_file_upload, True)
        self.assertEqual(imp.upload_filename, 'test.csv')
        self.assertEqual(imp.created_by, 'javerage')

        data = imp.json_data()
        self.assertEqual(len(data['assignments']), 2)
        self.assertEqual(len(data['errors']), 0)

    def test_create_from_list(self):
        imp = AssignmentImport.objects.create_from_list(
            sys_keys=[], created_by='javerage')
        self.assertEqual(imp.is_file_upload, False)

    def test_json_data(self):
        import1 = AssignmentImport(comment='comment', created_by='javerage')
        import1.save()

        data = import1.json_data()
        self.assertIsNotNone(data['id'])
        self.assertEqual(data['comment'], 'comment')
        self.assertEqual(data['is_file_upload'], True)
        self.assertIsNotNone(data['created_date'])
        self.assertEqual(data['created_by'], 'javerage')
        self.assertEqual(data['imported_date'], None)
        self.assertEqual(data['imported_status'], None)
        self.assertEqual(data['imported_message'], None)
        self.assertEqual(data['assignments'], [])
        self.assertEqual(data['errors'], [])

        # With assignments
        import1.document = self._csv([[1234567, 0, 2019, 4, 1, 123],
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

        imp.document = self._csv()
        a, errors = imp.assignments()
        self.assertEqual(len(a), 0)
        self.assertEqual(len(errors), 0)

        imp.document = self._csv([[1234567, 0, 2019, 4, 1, 123],
                                  [1234568, 0, 2019, 4, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 0)

        imp.document = self._csv([[1234567, 0, 2019, 4, 1, None],
                                  [1234568, 0, 2019, 4, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 1)

        imp.document = self._csv([[1234567, 0, None, 4, 1, 123],
                                  [1234568, 0, 2019, None, 1, 124]])
        a, errors = imp.assignments()
        self.assertEqual(len(a), 2)
        self.assertEqual(len(errors), 2)

        imp.document = b'<html>'
        self.assertRaises(TypeError, imp.assignments)
