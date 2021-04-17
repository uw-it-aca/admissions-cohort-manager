from cohort_manager.views.api import RESTDispatch
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from restclients_core.exceptions import DataFailureException
from userservice.user import UserService
from uw_saml.decorators import group_required
from cohort_manager.dao.adsel import submit_collection, _get_collection
from cohort_manager.models import PurpleGoldImport, SyskeyImport


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class SyskeyUploadView(RESTDispatch):
    def post(self, request, *args, **kwargs):
        user = UserService().get_acting_user()
        try:
            imp = None
            request_body = json.loads(request.body)
            is_purplegold = request_body.get("is_purplegold", False)
            if is_purplegold:
                imp = PurpleGoldImport.create_from_json(request_body, user)
                pass
            else:
                imp = SyskeyImport.create_from_json(request_body, user)
            content = imp.json_data()
            return self.json_response(status=200, content=content)
        except (AttributeError, IntegrityError) as ex:
            return self.error_response(status=400, message=ex)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class ModifySyskeyUploadView(RESTDispatch):
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
        user = UserService().get_original_user()
        is_purplegold = request_params.get('purplegold')

        try:
            upload = None
            if is_purplegold:
                upload = PurpleGoldImport.objects.get(id=upload_id)
            else:
                upload = SyskeyImport.objects.get(id=upload_id)
                if cohort_id:
                    upload.cohort = cohort_id
                if major_id:
                    upload.major = major_id
                upload.is_reassign = is_reassign
                upload.is_reassign_protected = is_reassign_protected
                upload.remove_assignments(ids_to_delete)

            # Using logged in user for bulk upload
            upload.created_by = user
            upload.is_submitted = is_submitted
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

    def get(self, request, upload_id, *args, **kwargs):
        try:
            apps = SyskeyImport.objects.get(id=upload_id)
            if apps.is_submitted:
                return self.error_response(400,
                                           message="Upload already submitted")
            return self.json_response(apps.json_data())
        except ValueError:
            return self.error_response(400,
                                       message="Invalid upload ID format")
        except SyskeyImport.DoesNotExist:
            return self.error_response(404,
                                       message="No uploads matching ID")
