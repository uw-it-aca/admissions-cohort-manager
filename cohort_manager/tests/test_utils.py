# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from cohort_manager.utils import to_csv


class UtilsTest(TestCase):
    def test_to_csv(self):
        self.assertEqual(to_csv(), '\n')
        self.assertEqual(to_csv([]), '\n')
        self.assertEqual(to_csv([1]), '1\n')
        self.assertEqual(to_csv(['a', 'b', 'c']), 'a,b,c\n')
