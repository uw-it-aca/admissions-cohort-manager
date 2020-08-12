import json
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db.utils import IntegrityError
from uw_saml.decorators import group_required
from cohort_manager.models import AssignmentImport, Assignment
from cohort_manager.dao.adsel import get_collection_by_id_type, \
    get_activity_log, get_collection_list_by_type, \
    get_apps_by_qtr_id_syskey_list, get_quarters_with_current, \
    submit_collection, get_applications_by_type_id_qtr, reset_collection,\
    _get_collection, get_application_from_bulk_upload
from cohort_manager.dao import InvalidCollectionException
from cohort_manager.utils import is_valid_auth_key
from userservice.user import UserService
from restclients_core.exceptions import DataFailureException


class RESTDispatch(View):
    @staticmethod
    def json_response(content={}, status=200):
        try:
            data = json.dumps(content,
                              sort_keys=True,
                              cls=DjangoJSONEncoder)
            return HttpResponse(data,
                                status=status,
                                content_type='application/json')
        except TypeError:
            return RESTDispatch().error_response(400)

    @staticmethod
    def error_response(status, message='', content={}):
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json',
                            )

    @staticmethod
    def no_auth_response():
        err_msg = "Authentication token not presented"
        response = HttpResponse(json.dumps({"error": err_msg}),
                                status=401,
                                content_type='application/json')
        response['WWW-Authenticate'] = "Bearer"
        return response


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
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
        user = UserService().get_original_user()
        import_args = {'quarter': qtr_id,
                       'campus': 0,
                       'comment': comment,
                       'created_by': user}
        if cohort_id:
            import_args['cohort'] = cohort_id
        if major_id:
            import_args['major'] = major_id

        try:
            assignment_import = AssignmentImport.objects.create(**import_args)
            if uploaded_file:
                document = None
                file = uploaded_file.read()
                try:
                    document = file.decode('utf-16')
                except UnicodeDecodeError as ex:
                    document = file.decode('utf-8')

                if document is None:
                    return self.error_response(status=400,
                                               message="Invalid document")
                assignment_import.document = document
                assignment_import.upload_filename = uploaded_file.name
                assignments = Assignment.create_from_file(assignment_import)
                if len(assignments) > 0:
                    Assignment.objects.bulk_create(assignments)
                else:
                    document = file.decode('ascii')
                    assignment_import.document = document
                    assignments = Assignment.create_from_file(
                        assignment_import)
                    Assignment.objects.bulk_create(assignments)

            if syskey_list:
                try:
                    applications = get_apps_by_qtr_id_syskey_list(qtr_id,
                                                                  syskey_list)
                except DataFailureException as ex:
                    return self.error_response(status=404, message=ex)
                Assignment.create_from_applications(assignment_import,
                                                    applications)
                assignment_import.is_file_upload = False

            assignment_import.save()
            content = assignment_import.json_data()
            return self.json_response(status=200, content=content)

        except (ValueError, IntegrityError) as ex:
            return self.error_response(status=400, message=ex)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class ModifyUploadView(RESTDispatch):
    def put(self, request, upload_id, *args, **kwargs):
        request_params = json.loads(request.body)
        is_reassign = request_params.get('is_reassign', False)
        is_reassign_protected = request_params.get('is_reassign_protected',
                                                   False)
        # reassign is required to be true to reassign protected
        if is_reassign_protected:
            is_reassign = True
        is_submitted = request_params.get('is_submitted', False)
        ids_to_delete = request_params.get('to_delete', [])
        comment = request_params.get('comment', '')
        major_id = request_params.get('major_id')
        cohort_id = request_params.get('cohort_id')

        try:
            upload = AssignmentImport.objects.get(id=upload_id)
            if cohort_id:
                upload.cohort = cohort_id
            if major_id:
                upload.major = major_id
            upload.is_submitted = is_submitted
            upload.is_reassign = is_reassign
            upload.is_reassign_protected = is_reassign_protected
            upload.remove_assignments(ids_to_delete)
            upload.comment = comment
            upload.save()
            response = upload.json_data()
            if is_submitted:
                (imp, post_body) = _get_collection(upload)
                response['request'] = post_body.json_data()
                try:
                    submission = submit_collection(upload)
                except DataFailureException as ex:
                    if "timeout" in str(ex):
                        return self.json_response(status=202,
                                                  content=response)
                    else:
                        return self.error_response(543, message=ex)
            return self.json_response(status=200, content=response)
        except ObjectDoesNotExist as ex:
            return self.error_response(404, message=ex)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
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

    def delete(self, request, quarter, collection_type,
               collection_id, *args, **kwargs):
        params = json.loads(request.body)
        comment = params.get('comment')
        user = UserService().get_original_user()
        try:
            apps = get_applications_by_type_id_qtr(collection_type,
                                                   collection_id, quarter)

            import_args = {'quarter': quarter,
                           'campus': 0,
                           'comment': comment,
                           'created_by': user}
            if collection_type == "cohort":
                import_args['cohort'] = 0
            if collection_type == "major":
                import_args['major'] = "none"

            assignment_import = AssignmentImport.objects.create(**import_args)
            Assignment.create_from_applications(assignment_import, apps)

            reset_collection(assignment_import, collection_type)

            return self.json_response()
        except Exception:
            return self.error_response(status=400)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class ActivityLog(RESTDispatch):
    def get(self, request, *args, **kwargs):
        activities = get_activity_log()
        return self.json_response(content={"activities": activities})


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class CollectionList(RESTDispatch):
    def get(self, request, collection_type, quarter):
        try:
            list = get_collection_list_by_type(collection_type, quarter)
            return self.json_response(list)
        except (InvalidCollectionException, DataFailureException) as ex:
            return self.error_response(status=400, message=ex)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
class BulkUpload(RESTDispatch):
    def post(self, request):
        req = json.loads(request.body)
        try:
            presented_token = request.headers['Authorization']
        except KeyError:
            return self.no_auth_response()
        if not is_valid_auth_key(presented_token):
            error = {'error': 'Invalid Authorization Key'}
            return self.error_response(status=403, content=error)

        # TODO: Switch to using file upload style if extra params are there
        applications = req['applications']
        cohort_id = req['cohort_id']
        major_id = req['major_id']

        import_args = {'quarter': req['admissions_period'],
                       'campus': applications[0]['campus'],
                       'created_by': "Tableau"}
        if cohort_id:
            import_args['cohort'] = cohort_id
        if major_id:
            import_args['major'] = major_id

        try:
            assignment_import = AssignmentImport.objects.create(**import_args)
            app_objects = get_application_from_bulk_upload(applications)
            Assignment.create_from_applications(assignment_import,
                                                app_objects)
            assignment_import.is_file_upload = False
            assignment_import.save()
            content = assignment_import.json_data()
            return self.json_response(status=200, content=content)
        except Exception:
            return self.error_response(status=500)
