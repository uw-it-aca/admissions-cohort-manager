import json
from django.test import TestCase, Client
from cohort_manager.views.api import RESTDispatch, UploadView, CollectionList
from cohort_manager.tests.views import TestViewApi


class RestDispatchTest(TestCase):
    def test_json_response(self):
        response = RESTDispatch.json_response('Test')
        self.assertEqual(response.content, b'"Test"')
        self.assertEqual(response.status_code, 200)

        response = RESTDispatch.json_response({'Test': 3, 'Another Test': 4})
        self.assertEqual(response.content, b'{"Another Test": 4, "Test": 3}')
        self.assertEqual(response.status_code, 200)

    def test_error_response(self):
        response = RESTDispatch.error_response(400, message='Error')
        self.assertEqual(response.content, b'{"error": "Error"}')
        self.assertEqual(response.status_code, 400)

        response = RESTDispatch.error_response(500, message=Exception('No'))
        self.assertEqual(response.content, b'{"error": "No"}')
        self.assertEqual(response.status_code, 500)


class UploadViewTest(TestCase):
    pass


class CollectionListTest(TestViewApi):
    def test_get_major_list(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        response = self.get_response('collection_list',
                                     kwargs={'collection_type': 'major',
                                             'quarter': 0})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content), 4)
        self.assertEqual(response_content[0]['value'], '0_BIOL_1')

    def test_get_cohort_list(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        response = self.get_response('collection_list',
                                     kwargs={'collection_type': 'cohort',
                                             'quarter': 0})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content), 2)
        self.assertEqual(response_content[0]['value'], 1)
