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
        uploaded_file = request.FILES['file']
        cohort_id = request.POST.get('cohort_id')
        major_id = request.POST.get('major_id')
        comment = request.POST.get('comment', "")

        # TODO: validate uploaded_file.content_type?

        assignment_import = AssignmentImport.objects.create_from_file(
            uploaded_file, created_by='TODO')
        if cohort_id:
            assignment_import.cohort = cohort_id
        if major_id:
            assignment_import.major = major_id
        assignment_import.comment = comment

        try:
            assignment_import.status_code = 200
            assignment_import.save()
            content = assignment_import.json_data()
            return self.json_response(status=200, content=content)

        except TypeError as ex:
            return self.error_response(status=400, content=ex)
