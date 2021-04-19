# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from cohort_manager.tests.views import TestViewApi


class SyskeyUploadViewTest(TestViewApi):
    def test_invalid_syskey(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        body = {'syskey_list': [1, 2],
                'comment': "foo",
                'qtr_id': 0,
                'cohort_id': 1}
        response = self.post_response("create_syskey_upload",
                                      json.dumps(body))
        response_content = json.loads(response.content)
        self.assertEqual(len(response_content['assignments']), 2)
        self.assertTrue(
            response_content['assignments'][0]['application_not_found'])

    def test_syskeys(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        body = {'syskey_list': [456340, 856340],
                'comment': "foo",
                'qtr_id': 0,
                'cohort_id': 1}
        response = self.post_response("create_syskey_upload",
                                      json.dumps(body))
        response_content = json.loads(response.content)
        self.assertEqual(len(response_content['assignments']), 3)
        self.assertEqual(response_content['comment'], body['comment'])
        self.assertEqual(response_content['cohort'], body['cohort_id'])
        self.assertIsNone(response_content['major'])
        adsel_id = response_content['assignments'][0]['admission_selection_id']
        self.assertEqual(adsel_id, 54687)

    def test_error(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        body = {'cohort_id': 1}
        response = self.post_response("create_syskey_upload",
                                      json.dumps(body))
        self.assertEqual(response.status_code, 400)


class SyskeyModifyUploadViewTest(TestViewApi):
    upload_response = None
    upload_body = {'syskey_list': [456340, 856340],
                   'comment': "foo",
                   'qtr_id': 0,
                   'cohort_id': 1}

    def setUp(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        body = self.upload_body
        response = self.post_response("create_syskey_upload",
                                      json.dumps(body))
        self.upload_response = json.loads(response.content)

    def test_get_upload(self):
        response = self.get_response("modify_syskey_upload",
                                     kwargs={"upload_id":
                                             self.upload_response['id']})
        modify_response = json.loads(response.content)
        self.assertEqual(len(modify_response['assignments']), 3)

    def test_get_bad(self):
        response = self.get_response("modify_syskey_upload",
                                     kwargs={"upload_id": "FOO"})
        self.assertEqual(response.status_code, 400)

    def test_missing(self):
        response = self.get_response("modify_syskey_upload",
                                     kwargs={"upload_id": 42})
        self.assertEqual(response.status_code, 404)

    def test_already_submitted(self):
        body = self.upload_body
        body['is_submitted'] = True
        response = self.put_response("modify_syskey_upload",
                                     json.dumps(body),
                                     kwargs={"upload_id":
                                             self.upload_response['id']})
        response = self.get_response("modify_syskey_upload",
                                     kwargs={"upload_id": 1})
        self.assertEqual(response.status_code, 400)

    def test_remove_application(self):
        response = self.put_response("modify_syskey_upload",
                                     json.dumps({"to_delete": [54687]}),
                                     kwargs={"upload_id":
                                             self.upload_response['id']})
        modify_response = json.loads(response.content)
        self.assertEqual(len(modify_response['assignments']), 2)
        new_adsel_ids = [a['admission_selection_id'] for a
                         in modify_response['assignments']]
        self.assertEqual(new_adsel_ids, [84136, 17508])

    def test_submit(self):
        body = self.upload_body
        body['is_submitted'] = True
        body['is_reassign'] = True
        body['is_reassign_protected'] = True
        response = self.put_response("modify_syskey_upload",
                                     json.dumps(body),
                                     kwargs={"upload_id":
                                             self.upload_response['id']})
        self.assertEqual(response.status_code, 200)

    def test_submit_bad(self):
        response = self.put_response("modify_syskey_upload",
                                     json.dumps(self.upload_body),
                                     kwargs={"upload_id": 42})
        self.assertEqual(response.status_code, 404)
