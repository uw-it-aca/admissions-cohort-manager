from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from cohort_manager.models import AssignmentImport, Assignment, SyskeyImport
from uw_adsel.models import Application
from cohort_manager.utils import to_csv
from datetime import datetime
import os


class SyskeyImportTest(TestCase):
    def test_create_from_list(self):
        upload_body = {
            'comment': "This is a comment",
            'qtr_id': 0,
            'cohort_id': 52,
            'syskey_list': [656340, 456340, 97508]
        }

        import_object = SyskeyImport.create_from_json(upload_body, 'javerage')
        self.assertEqual(import_object.comment, upload_body['comment'])
        self.assertEqual(import_object.quarter, upload_body['qtr_id'])
        self.assertEqual(import_object.cohort, upload_body['cohort_id'])
        self.assertIsNone(import_object.major)
        self.assertFalse(import_object.is_purplegold)


class AssignmentTest(TestCase):
    def setUp(self):
        self.assignment = Assignment(
            system_key='1',
            application_number='8',
            admission_selection_id='000',
            sdb_app_status=12)
        self.assignment_reassign = Assignment(
            system_key='1',
            application_number='8',
            admission_selection_id='000',
            assigned_cohort=32,
            assigned_major="CSE")

    def test_json_data(self):
        self.assertEqual(self.assignment.json_data(), {
            'admission_selection_id': '000',
            'application_number': '8',
            'system_key': '1',
            'assigned_cohort': None,
            'assigned_major': None,
            'campus': "Seattle",
            'sdb_app_status': 12})
        self.assertEqual(self.assignment_reassign.json_data(), {
            'admission_selection_id': '000',
            'application_number': '8',
            'system_key': '1',
            'assigned_cohort': 32,
            'assigned_major': "CSE",
            'campus': "Seattle",
            'sdb_app_status': None})


class AssignmentImportTest(TestCase):

    # TODO: Figure out how to make file based tests mockable
    # def test_create_from_file(self):
    #     test_apps = [["SMITH,JOHN LEE", "4126156", "1", "M", "", "",
    #                   "Non-Resident", "", "7", "0.00", "False", "True",
    #                   "0", "Biochemistry", "College of Arts and Sciences",
    #                   "Biochemistry", "College of Arts and Sciences",
    #                   "", "CO",
    #                   "0", "0", "0", "0", "0", "0", "0", "0", "0", "0",
    #                   "60269",
    #                   "CO SAMPLE SCH", "060269", "SAMPLE SCH", "COLORADO SP",
    #                   "CO", "", "", "", "", "35734"],
    #                  ["JONES,FRED ALLEN", "1534694", "1", "F", "", "",
    #                  "Resident", "97", "13", "2.75", "True", "True", "0",
    #                  "", "", "", "", "", "WA", "7", "7", "14", "0", "0",
    #                   "0", "0", "0", "5", "0", "481137", "TEST H S",
    #                   "481137", "TEST H S", "SEATTLE", "WA", "", "", "", "",
    #                   "44671"],
    #                  ["AVERAGE,JAMES STUDENT", "8471266", "1", "F", "", "",
    #                   "Non-Resident", "97", "13", "2.75", "True", "True"
    #                   , "0",
    #                   "", "", "", "", "", "CA", "8", "8", "10", "0", "0",
    #                   "0",
    #                   "0", "0", "5", "0", "50715", "SUPER H S", "050715",
    #                   "SUPER H S", "SEATTLE", "CA", "", "", "", "", "32732"]]
    #     file_data = self._csv(test_apps)
    #
    #     uploaded_file = SimpleUploadedFile(
    #         'test.csv', file_data.encode(), content_type='text/csv')
    #
    #     imp = AssignmentImport.objects.create_from_file(
    #         uploaded_file=uploaded_file, created_by='javerage')
    #     self.assertEqual(imp.is_file_upload, True)
    #     self.assertEqual(imp.upload_filename, 'test.csv')
    #     self.assertEqual(imp.created_by, 'javerage')
    #
    #     data = imp.json_data()
    #     self.assertEqual(len(data['assignments']), 2)
    #     self.assertEqual(len(data['errors']), 0)

    def test_create_from_list(self):
        a1 = Application(
            adsel_id=51231,
            application_number=0,
            system_key=123,
            campus=1,
            quarter_id=0,
            assigned_cohort=31,
            assigned_major="CSE"
        )
        a2 = Application(
            adsel_id=51241,
            application_number=1,
            system_key=123,
            campus=1,
            quarter_id=0,
            assigned_cohort=31,
            assigned_major="CSE"
        )

        import_args = {'quarter': 20194,
                       'campus': 'SEA',
                       'comment': "this is an import",
                       'created_by': "javerage",
                       'cohort': 21,
                       'is_file_upload': False}

        imp = AssignmentImport.objects.create(**import_args)

        Assignment.create_from_applications(imp, [a1, a2])
        assignments = imp.assignment_set.all()
        self.assertEqual(len(assignments), 2)

    def test_json_data(self):
        a1 = Application(
            adsel_id=51231,
            application_number=0,
            system_key=123,
            campus=1,
            quarter_id=0,
            assigned_cohort=31,
            assigned_major="CSE"
        )
        a2 = Application(
            adsel_id=51241,
            application_number=1,
            system_key=123,
            campus=1,
            quarter_id=0,
            assigned_cohort=31,
            assigned_major="CSE"
        )

        import_args = {'quarter': 20194,
                       'campus': 'SEA',
                       'comment': "this is an import",
                       'created_by': "javerage",
                       'cohort': 21,
                       'is_file_upload': False}

        imp = AssignmentImport.objects.create(**import_args)

        Assignment.create_from_applications(imp, [a1, a2])

        data = imp.json_data()
        self.assertEqual(len(data['assignments']), 2)

    # def test_assignment_errors(self):
    #     imp = AssignmentImport()
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 0)
    #     self.assertEqual(len(errors), 0)
    #
    #     imp.document = None
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 0)
    #     self.assertEqual(len(errors), 0)
    #
    #     imp.document = self._csv()
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 0)
    #     self.assertEqual(len(errors), 0)
    #
    #     imp.document = self._csv([[1234567, 0, 2019, 4, 1, 123],
    #                               [1234568, 0, 2019, 4, 1, 124]])
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 2)
    #     self.assertEqual(len(errors), 0)
    #
    #     imp.document = self._csv([[1234567, 0, 2019, 4, 1, None],
    #                               [1234568, 0, 2019, 4, 1, 124]])
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 2)
    #     self.assertEqual(len(errors), 1)
    #
    #     imp.document = self._csv([[1234567, 0, None, 4, 1, 123],
    #                               [1234568, 0, 2019, None, 1, 124]])
    #     a, errors = imp.assignments()
    #     self.assertEqual(len(a), 2)
    #     self.assertEqual(len(errors), 2)
    #
    #     imp.document = b'<html>'
    #     self.assertRaises(TypeError, imp.assignments)
    #
    # def test_remove_assignments(self):
    #     file_data = self._csv([[1234567, 0, 2019, 4, 1, 123],
    #                            [1234568, 0, 2019, 4, 1, 124]])
    #
    #     uploaded_file = SimpleUploadedFile(
    #         'test.csv', file_data.encode(), content_type='text/csv')
    #
    #     imp = AssignmentImport.objects.create_from_file(
    #         uploaded_file=uploaded_file, created_by='javerage')
    #     assignments, errors = imp.assignments()
    #     self.assertEqual(len(assignments), 2)
    #     imp.remove_assignments("124")
    #     assignments, errors = imp.assignments()
    #     self.assertEqual(len(assignments), 1)
