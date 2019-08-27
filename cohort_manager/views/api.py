from django.http import HttpResponse
from django.views import View
from cohort_manager.models import AssignmentImport
import json


class RESTDispatch(View):
    @staticmethod
    def json_response(content='', status=200):
        return HttpResponse(json.dumps(content, sort_keys=True),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def error_response(status, message='', content={}):
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json')


class UploadView(RESTDispatch):
    def post(self, request, *args, **kwargs):
        upload_file = request.FILES['file']

        assignment_import = AssignmentImport(
            document=upload_file.read().decode('utf-8'),
            created_by='TODO')

        try:
            assignment_import.status_code = 200
            assignment_import.save()
            content = assignment_import.json_data()
            return self.json_response(status=200, content=content)

        except TypeError as ex:
            return self.error_response(status=400, content=ex)
