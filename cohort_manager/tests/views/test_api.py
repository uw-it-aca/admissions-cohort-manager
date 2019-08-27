from django.test import TestCase
from cohort_manager.views.api import RESTDispatch, UploadView


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
