from django.urls import path, re_path
from cohort_manager.views import PurpleGoldEmbed
from cohort_manager.views.api import UploadView, CollectionDetails, \
    ActivityLog, CollectionList, ModifyUploadView, PeriodList, BulkUpload, \
    MockDataView
from cohort_manager.views.pages import LandingView, AdminView
from django.conf import settings

urlpatterns = [
    re_path(r'api/v1/bulk_upload/', BulkUpload.as_view(), name="bulk_upload"),
    re_path(r'api/upload/(?P<upload_id>.*)/',
            ModifyUploadView.as_view(),
            name="upload"),
    path('api/upload',
         UploadView.as_view(),
         name="create_upload"),
    re_path(r'^api/collection/(?P<collection_type>.*)/'
            r'(?P<quarter>.*)/(?P<collection_id>.+)/',
            CollectionDetails.as_view()),
    re_path(r'^api/collection/(?P<collection_type>.*)/(?P<quarter>.*)/',
            CollectionList.as_view(),
            name="collection_list"),
    re_path(r'^api/activity/',
            ActivityLog.as_view()),
    re_path(r'^api/periods/',
            PeriodList.as_view()),
    re_path(r'^purplegold_embed/',
            PurpleGoldEmbed.as_view()),
    re_path(r'^.*$', LandingView.as_view()),
]
if settings.DEBUG:
    urlpatterns.insert(0, re_path(r'api/admin/mock_data/',
                                  MockDataView.as_view(),
                                  name="bulk_upload"))
    urlpatterns.insert(0, re_path(r'^admin/', AdminView.as_view()))
