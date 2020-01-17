from django.test import TestCase
from cohort_manager.dao.adsel import get_collection_by_id_type, \
    get_applications_by_cohort_qtr, get_applications_by_major_qtr, \
    get_quarters_with_current, get_applications_by_type_id_qtr, \
    get_activity_log, get_application_by_qtr_syskey,\
    get_apps_by_qtr_id_syskey_list, submit_collection, reset_collection
from cohort_manager.dao import InvalidCollectionException
from cohort_manager.models import AssignmentImport, Assignment


class RestDispatchTest(TestCase):
    def test_cohort(self):
        resp = get_collection_by_id_type(1, "cohort", 0)
        self.assertEqual(resp['applications_assigned'], 120)
        self.assertIsNotNone(get_collection_by_id_type(2, "cohort", 0))
        self.assertIsNone(get_collection_by_id_type(1234, "cohort", 0))

    def test_major(self):
        resp = get_collection_by_id_type("BIOL", "major", 0)
        self.assertEqual(resp['applications_assigned'], 32)
        self.assertIsNotNone(get_collection_by_id_type("CHEM", "major", 0))
        self.assertIsNone(get_collection_by_id_type("FOOBAR", "major", 0))

    def test_invalid_collection(self):
        with self.assertRaises(InvalidCollectionException):
            get_collection_by_id_type(123, "FOOBAR", 0)

    def test_apps_by_cohort(self):
        apps = get_applications_by_cohort_qtr(2, 0)
        self.assertEqual(len(apps), 2)

        apps = get_applications_by_cohort_qtr(1, 0)
        self.assertEqual(len(apps), 1)

        apps = get_applications_by_cohort_qtr(1, 1)
        self.assertEqual(len(apps), 0)

    def test_apps_by_major(self):
        apps = get_applications_by_major_qtr("string", 0)
        self.assertEqual(len(apps), 4)

        apps = get_applications_by_major_qtr("test", 0)
        self.assertEqual(len(apps), 0)

        apps = get_applications_by_major_qtr("test", 99)
        self.assertEqual(len(apps), 0)

    def test_quarters(self):
        quarters = get_quarters_with_current()
        self.assertEqual(len(quarters), 2)

    def test_get_apps_by_type(self):
        apps = get_applications_by_type_id_qtr("cohort", 1, 0)
        self.assertEqual(len(apps), 1)
        apps = get_applications_by_type_id_qtr("major", "string", 0)
        self.assertEqual(len(apps), 4)

    def test_activity_log(self):
        activities = get_activity_log()
        self.assertEqual(len(activities), 4)

    def test_app_by_qtr_syskey(self):
        app = get_application_by_qtr_syskey(0, 123)
        self.assertEqual(len(app), 4)

    def test_app_by_qtr_syskey_list(self):
        app = get_apps_by_qtr_id_syskey_list(0, [123, 0])
        self.assertEqual(len(app), 4)

    def test_submit_cohort(self):
        import_args = {'quarter': 0,
                       'campus': 0,
                       'comment': "my comment",
                       'created_by': "javerage",
                       'cohort': "1",
                       'is_file_upload': False}

        assignment_import = AssignmentImport.objects.create(**import_args)
        app = get_application_by_qtr_syskey(0, 123)
        Assignment.create_from_applications(assignment_import, app)
        assignment_import.save()
        submit_collection(assignment_import)
        self.assertTrue(assignment_import.is_submitted)

    def test_submit_major(self):
        import_args = {'quarter': 0,
                       'campus': 0,
                       'comment': "my comment",
                       'created_by': "javerage",
                       'major': "CSE",
                       'is_file_upload': False}

        assignment_import = AssignmentImport.objects.create(**import_args)
        app = get_application_by_qtr_syskey(0, 123)
        Assignment.create_from_applications(assignment_import, app)
        assignment_import.save()
        submit_collection(assignment_import)
        self.assertTrue(assignment_import.is_submitted)

    def test_reset_cohort(self):
        import_args = {'quarter': 0,
                       'campus': 0,
                       'comment': "my comment",
                       'created_by': "javerage",
                       'cohort': "1",
                       'is_file_upload': False}

        assignment_import = AssignmentImport.objects.create(**import_args)
        try:
            reset_collection(assignment_import, "cohort")
        except Exception:
            self.fail('reset_collection() raised an exception unexpectedly')

    def test_reset_major(self):
        import_args = {'quarter': 0,
                       'campus': 0,
                       'comment': "my comment",
                       'created_by': "javerage",
                       'major': "CSE",
                       'is_file_upload': False}

        assignment_import = AssignmentImport.objects.create(**import_args)
        try:
            reset_collection(assignment_import, "major")
        except Exception:
            self.fail('reset_collection() raised an exception unexpectedly')
