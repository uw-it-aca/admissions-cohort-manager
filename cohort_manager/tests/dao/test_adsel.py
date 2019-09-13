from django.test import TestCase
from cohort_manager.dao.adsel import get_collection_by_id_type
from cohort_manager.dao import InvalidCollectionException


class RestDispatchTest(TestCase):
    def test_cohort(self):
        resp = get_collection_by_id_type(1, "cohort")
        self.assertEqual(resp['applications_assigned'], 412)
        self.assertIsNotNone(get_collection_by_id_type(2, "cohort"))
        self.assertIsNotNone(get_collection_by_id_type(99, "cohort"))
        self.assertIsNone(get_collection_by_id_type(1234, "cohort"))

    def test_major(self):
        resp = get_collection_by_id_type("CSE", "major")
        self.assertEqual(resp['applications_assigned'], 543)
        self.assertIsNotNone(get_collection_by_id_type("CHEM", "major"))
        self.assertIsNotNone(get_collection_by_id_type("ART H", "major"))
        self.assertIsNone(get_collection_by_id_type("FOOBAR", "major"))

    def test_invalid_collection(self):
        with self.assertRaises(InvalidCollectionException):
            get_collection_by_id_type(123, "FOOBAR")
