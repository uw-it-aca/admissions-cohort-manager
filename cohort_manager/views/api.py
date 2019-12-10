import json
from django.conf import settings
from django.http import HttpResponse, QueryDict
from django.views import View
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from uw_saml.decorators import group_required
from cohort_manager.models import AssignmentImport
from cohort_manager.dao.adsel import get_collection_by_id_type, \
    get_activity_log, get_collection_list_by_type, \
    get_apps_by_qtr_id_syskey_list, get_quarters_with_current, \
    submit_collection
from cohort_manager.dao import InvalidCollectionException


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class RESTDispatch(View):
    @staticmethod
    def json_response(content={}, status=200):
        return HttpResponse(json.dumps(content,
                                       sort_keys=True,
                                       cls=DjangoJSONEncoder),
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
        uploaded_file = request.FILES.get('file')
        try:
            syskey_list = request.POST.get('syskey_list').split(",")
        except AttributeError:
            syskey_list = None
        cohort_id = request.POST.get('cohort_id')
        major_id = request.POST.get('major_id')
        comment = request.POST.get('comment', "")
        qtr_id = request.POST.get('qtr_id', "")

        # TODO: validate uploaded_file.content_type?
        if uploaded_file:
            assignment_import = AssignmentImport.objects.create_from_file(
                uploaded_file, created_by='TODO')
        if syskey_list:
            applications = get_apps_by_qtr_id_syskey_list(qtr_id, syskey_list)
            assignment_import = AssignmentImport.objects.create_from_list(
                applications, created_by='TODO'
            )
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
            return self.error_response(status=400, message=ex)


class ModifyUploadView(RESTDispatch):
    def put(self, request, upload_id, *args, **kwargs):
        request_params = json.loads(request.body)
        is_reassign = request_params.get('is_reassign', False)
        is_reassign_protected = request_params.get('is_reassign_protected',
                                                   False)
        is_submitted = request_params.get('is_submitted', False)
        ids_to_delete = request_params.get('to_delete', [])
        try:
            upload = AssignmentImport.objects.get(id=upload_id)
            upload.is_submitted = is_submitted
            upload.is_reassign = is_reassign
            upload.is_reassign_protected = is_reassign_protected
            upload.remove_assignments(ids_to_delete)
            upload.save()
            if is_submitted:
                submit_collection(upload)
            return self.json_response(status=200, content=upload.json_data())
        except ObjectDoesNotExist as ex:
            return self.error_response(404, message=ex)


class CollectionDetails(RESTDispatch):
    def get(self, request, collection_type, collection_id, quarter,
            *args, **kwargs):
        try:
            response = get_collection_by_id_type(collection_id,
                                                 collection_type,
                                                 quarter)
            if response is not None:
                return self.json_response(status=200, content=response)
            else:
                return self.error_response(status=404,
                                           message="Collection Not Found")
        except InvalidCollectionException as ex:
            return self.error_response(status=400, message=ex)

    def delete(self, request, collection_type, collection_id, *args, **kwargs):
        params = json.loads(request.body)
        comment = params.get('comment')
        return self.json_response()


class ActivityLog(RESTDispatch):
    def get(self, request, *args, **kwargs):
        activities = get_activity_log()
        return self.json_response(content={"activities": activities})


class CollectionList(RESTDispatch):
    def get(self, request, collection_type, quarter):
        try:
            list = get_collection_list_by_type(collection_type, quarter)
            return self.json_response(list)
        except InvalidCollectionException as ex:
            return self.error_response(status=400, message=ex)


class PeriodList(RESTDispatch):
    def get(self, request):
        quarters = get_quarters_with_current()
        resp = []
        for quarter in quarters:
            resp.append({'value': quarter.id,
                         'text': "{} {}".format(quarter.appl_qtr,
                                                quarter.appl_yr),
                         'current': quarter.is_current})
        return self.json_response(status=200, content=resp)
