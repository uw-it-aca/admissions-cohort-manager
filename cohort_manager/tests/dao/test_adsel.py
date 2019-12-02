from django.test import TestCase
from cohort_manager.dao.adsel import get_collection_by_id_type
from cohort_manager.dao import InvalidCollectionException


class RestDispatchTest(TestCase):
    def test_cohort(self):
        resp = get_collection_by_id_type(1, "cohort", 0)
        self.assertEqual(resp['applications_assigned'], 120)
        self.assertIsNotNone(get_collection_by_id_type(2, "cohort", 0))
        self.assertIsNone(get_collection_by_id_type(1234, "cohort", 0))

    def test_major(self):
        resp = get_collection_by_id_type("CSE", "major", 0)
        self.assertEqual(resp['applications_assigned'], 32)
        self.assertIsNotNone(get_collection_by_id_type("CHEM", "major", 0))
        self.assertIsNone(get_collection_by_id_type("FOOBAR", "major", 0))

    def test_invalid_collection(self):
        with self.assertRaises(InvalidCollectionException):
            get_collection_by_id_type(123, "FOOBAR", 0)
