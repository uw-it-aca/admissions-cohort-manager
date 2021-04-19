# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from cohort_manager.dao.adsel import get_collection_by_id_type, \
    get_applications_by_cohort_qtr, get_applications_by_major_qtr
from cohort_manager.dao import InvalidCollectionException


class RestDispatchTest(TestCase):
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
