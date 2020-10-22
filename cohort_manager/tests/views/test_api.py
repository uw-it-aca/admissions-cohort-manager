import json
from django.test import TestCase, Client
from django.core.exceptions import ImproperlyConfigured
from cohort_manager.views.api import RESTDispatch, UploadView, CollectionList
from cohort_manager.tests.views import TestViewApi
from cohort_manager.models import AssignmentImport


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
        self.assertEqual(len(response_content), 6)
        self.assertEqual(response_content[0]['value'], 1)


class BulkUploadTest(TestViewApi):
    cohort_assignment = {
        "admissions_period": 20203,
        "major_id": None,
        "cohort_id": 21,
        "created_by": "javerage",
        "applications": [{
            "admission_selection_id": "33450",
            "application_number": 1,
            "assigned_cohort": 0,
            "assigned_major": None,
            "campus": "Seattle",
            "sdb_app_status": 12,
            "system_key": "2122786"
        }, {
            "admission_selection_id": "20718",
            "application_number": 1,
            "assigned_cohort": 35,
            "assigned_major": "0_A A_00_1_6",
            "campus": "Seattle",
            "sdb_app_status": 14,
            "system_key": "2107788"
        }
        ]}
    FAKE_API_TOKEN = 'FoObArBaZ123!$%'

    def test_upload(self):
        with self.settings(API_TOKEN=self.FAKE_API_TOKEN):
            token_str = "Bearer %s" % self.FAKE_API_TOKEN
            self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                                 HTTP_AUTHORIZATION=token_str)

            response = self.post_response('bulk_upload',
                                          json.dumps(self.cohort_assignment))
            content = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content['aat_url'],
                             "http://testserver/iframe/bulk_view/1")
            upload = AssignmentImport.objects.get(id=1)
            self.assertIsNotNone(upload)
            self.assertEqual(upload.cohort, "21")

    def test_auth_failures(self):
        with self.settings(API_TOKEN=self.FAKE_API_TOKEN):
            token_str = "Bearer %s" % "BadToken"
            self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                                 HTTP_AUTHORIZATION=token_str)

            response = self.post_response('bulk_upload',
                                          json.dumps(self.cohort_assignment))
            self.assertEqual(response.status_code, 403)

            self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
            response = self.post_response('bulk_upload',
                                          json.dumps(self.cohort_assignment))
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response['WWW-Authenticate'], "Bearer")


class ListUploadTest(TestViewApi):
    def test__invalid_syskey(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        body = {'syskey_list': "1,2,123",
                'comment': "foo",
                'qtr_id': 0,
                'cohort_id': 1}
        response = self.post_form_response("create_upload", body)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['invalid_syskeys'][0], '1')
        self.assertEqual(len(response_content['invalid_syskeys']), 2)


class ModifyUploadViewTest(TestViewApi):
    def test_get_upload(self):
        upload = AssignmentImport(cohort=42, created_by="javerage", quarter=1)
        upload.save()
        request = self.get_request('/', 'javerage', 'u_test_group')
        response = self.get_response("upload", kwargs={"upload_id": 1})
        response_content = json.loads(response.content)
        self.assertEqual(response_content['created_by'], "javerage")
        self.assertEqual(response_content['cohort'], "42")
