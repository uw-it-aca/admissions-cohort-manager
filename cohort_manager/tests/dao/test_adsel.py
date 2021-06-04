# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from cohort_manager.dao.adsel import get_collection_by_id_type, \
    get_applications_by_cohort_qtr, get_applications_by_major_qtr, \
    get_current_quarters, get_applications_by_type_id_qtr, get_activity_log, \
    get_collection_list_by_type, get_application_by_qtr_syskey, \
    get_apps_by_qtr_id_syskey_list, _get_collection, submit_collection, \
    reset_purplegold, reset_collection, get_application_from_bulk_upload

from cohort_manager.models import SyskeyImport, PurpleGoldImport, \
    AssignmentImport, Assignment

from cohort_manager.dao import InvalidCollectionException


class RestDispatchTest(TestCase):
    def create_cohort_import(self):
        upload_body = {
            'comment': "This is a comment",
            'qtr_id': 0,
            'cohort_id': 52,
            'syskey_list': [656340, 456340, 97508],
        }
        return SyskeyImport.create_from_json(upload_body, 'javerage')

    def create_major_import(self):
        upload_body = {
            'comment': "This is a comment",
            'qtr_id': 0,
            'major_id': "0_BIOL_1",
            'syskey_list': [656340, 456340, 97508]
        }
        return SyskeyImport.create_from_json(upload_body, 'javerage')

    def create_pg_import(self):
        upload_body = {
            'comment': "This is a comment",
            'qtr_id': 0,
            'cohort_id': 52,
            'assignments': [
                {'admissionSelectionID': 20154,
                 'awardAmount': 2123.12},
                {'admissionSelectionID': 12341,
                 'awardAmount': 24362.12},
                {'admissionSelectionID': 31521,
                 'awardAmount': 622.12},
                {'admissionSelectionID': 34567,
                 'awardAmount': 552.12},
                {'admissionSelectionID': 87532,
                 'awardAmount': 324.12},
            ]
        }
        return PurpleGoldImport().create_from_json(upload_body, 'javerage')

    def test_cohort(self):
        resp = get_collection_by_id_type(1, "cohort", 0)
        self.assertEqual(resp['applications_assigned'], 120)
        self.assertIsNotNone(get_collection_by_id_type(81, "cohort", 0))
        self.assertIsNone(get_collection_by_id_type(1234, "cohort", 0))

    def test_major(self):
        resp = get_collection_by_id_type("0_BIOL_1", "major", 0)
        self.assertEqual(resp['applications_assigned'], 32)
        self.assertEqual(resp['assigned_resident'], 12412)
        self.assertEqual(resp['assigned_nonresident'], 6)
        self.assertEqual(resp['assigned_international'], 0)

        self.assertIsNotNone(get_collection_by_id_type("0_CHEM_1", "major", 0))
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
        apps = get_applications_by_major_qtr(None, 0)
        self.assertEqual(len(apps), 4)

        apps = get_applications_by_major_qtr("test", 0)
        self.assertEqual(len(apps), 0)

        apps = get_applications_by_major_qtr("test", 42)
        self.assertIsNone(apps)

    def test_get_quarters(self):
        quarters = get_current_quarters()
        self.assertEqual(len(quarters), 3)

    def test_get_applications_by_type_id_qtr(self):
        apps = get_applications_by_type_id_qtr("cohort", 2, 0)
        self.assertEqual(len(apps), 2)

        apps = get_applications_by_type_id_qtr("major", None, 0)
        self.assertEqual(len(apps), 4)

        apps = get_applications_by_type_id_qtr("purplegold", None, 0)
        self.assertEqual(len(apps), 4)

    def test_get_activity_log(self):
        act = get_activity_log(netid="javerage")
        self.assertEqual(len(act), 2)
        self.assertEqual(act[0]['user'], 'javerage')

    def test_get_collection_list_by_type(self):
        list = get_collection_list_by_type("major", 0)
        self.assertEqual(len(list), 4)
        self.assertEqual(list[0]['value'], "0_BIOL_1")

        list = get_collection_list_by_type("cohort", 0)
        self.assertEqual(len(list), 6)
        self.assertEqual(list[0]['value'], 1)

        list = get_collection_list_by_type("dd", 0)
        self.assertEqual(len(list), 5)
        self.assertEqual(list[0]['value'], "0_foo_1")

        with self.assertRaises(InvalidCollectionException):
            get_collection_list_by_type("foo", 1)

    def test_get_application_by_qtr_syskey(self):
        app = get_application_by_qtr_syskey(0, 123)
        self.assertEqual(len(app), 4)

    def test_get_apps_by_qtr_id_syskey_list(self):
        syskeys = [123, 76711, 656340]
        (apps, invalid) = get_apps_by_qtr_id_syskey_list(0, syskeys)
        self.assertEqual(len(apps), 4)
        self.assertEqual(len(invalid), 2)

    def test_get_collection(self):
        import_object = self.create_cohort_import()
        (a_import, assignment) = _get_collection(import_object)
        self.assertEqual(assignment.cohort_number, 52)

        import_object = self.create_major_import()
        (a_import, assignment) = _get_collection(import_object)
        self.assertEqual(assignment.major_code, "0_BIOL_1")

        pg_import = self.create_pg_import()
        (a_import, assignment) = _get_collection(pg_import)
        self.assertEqual(len(assignment.applicants), 5)

    def test_submit_collection(self):
        cohort = submit_collection(self.create_cohort_import())
        major = submit_collection(self.create_major_import())
        pg = submit_collection(self.create_pg_import())
        self.assertEqual(cohort['response']['summaryPostStatus'], 'string')
        self.assertEqual(major['response']['summaryPostStatus'], 'string')
        self.assertEqual(pg['response']['summaryPostStatus'], 'string')

    def test_reset_collection(self):
        apps = get_applications_by_type_id_qtr("major", None, 0)
        import_args = {'quarter': int(1),
                       'campus': 0,
                       'comment': 'comment',
                       'created_by': 'user'}
        assignment_import = \
            AssignmentImport.objects.create(**import_args)
        Assignment.create_from_applications(assignment_import, apps)
        major = reset_collection(assignment_import, "major")
        self.assertEqual(major['response']['summaryPostStatus'], 'string')

        apps = get_applications_by_type_id_qtr("cohort", 1, 0)
        import_args = {'quarter': 1,
                       'campus': 0,
                       'comment': 'comment',
                       'created_by': 'user',
                       'cohort': 0}
        assignment_import = \
            AssignmentImport.objects.create(**import_args)
        Assignment.create_from_applications(assignment_import, apps)
        cohort = reset_collection(assignment_import, "cohort")
        self.assertEqual(cohort['response']['summaryPostStatus'], 'string')

    def test_reset_purplegold(self):
        import_args = {'quarter': 1,
                       'campus': 0,
                       'comment': 'comment',
                       'created_by': 'user',
                       }
        apps = get_applications_by_type_id_qtr("purplegold", None, 0)
        reset = reset_purplegold(import_args, apps)
        self.assertEqual(reset['response']['summaryPostStatus'], 'string')

    def test_get_application_from_bulk_upload(self):
        upload = [{
            'admission_selection_id': 4221344,
            'application_number': 1,
            'assigned_cohort': 23,
            'assigned_major': None,
            'campus': 'Seattle',
            'system_key': 312
        }]
        apps = get_application_from_bulk_upload(upload)
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].adsel_id, 4221344)
