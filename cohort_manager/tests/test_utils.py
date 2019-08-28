from django.test import TestCase
from cohort_manager.utils import to_csv


class UtilsTest(TestCase):
    def test_to_csv(self):
        self.assertEqual(to_csv(), '\n')
        self.assertEqual(to_csv([]), '\n')
        self.assertEqual(to_csv([1]), '1\n')
        self.assertEqual(to_csv(['a', 'b', 'c']), 'a,b,c\n')
