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


class UploadView(RESTDispatch):
    def post(self, request, *args, **kwargs):
        upload_file = request.FILES['file']

        assignment_import = AssignmentImport(
            document=upload_file.read().decode('utf-8'),
            imported_by='TODO')

        status = 200
        try:
            content = assignment_import.json_data()
            assignment_import.status_code = status
            assignment_import.save()

        except TypeError as ex:
            content = ex
            status = 400

        return self.json_response(status=status, content=content)
