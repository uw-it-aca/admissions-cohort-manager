from django.urls import path, re_path

from cohort_manager.views.api import UploadView, CollectionDetails, \
    ActivityLog, CollectionList, ModifyUploadView, PeriodList, BulkUpload
from cohort_manager.views.pages import LandingView, BulkView

urlpatterns = [
    re_path(r'api/v1/bulk_upload/', BulkUpload.as_view(), name="bulk_upload"),
    re_path(r'api/upload/(?P<upload_id>.*)/',
            ModifyUploadView.as_view(),
            name="upload"),
    path('api/upload', UploadView.as_view()),
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
    re_path(r'^.*$', LandingView.as_view()),
]
