from __future__ import unicode_literals
from django.apps import AppConfig
from restclients_core.dao import MockDAO
import os


class CohortManagerConfig(AppConfig):
    name = 'cohort_manager'

    def ready(self):
        cohort_manager_mocks = os.path.join(os.path.dirname(__file__),
                                            "resources")
        MockDAO.register_mock_path(cohort_manager_mocks)
