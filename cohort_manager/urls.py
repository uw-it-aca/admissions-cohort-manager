from django.urls import path, re_path

from cohort_manager.views.api import UploadView, CollectionDetails, \
    ActivityLog, CollectionList, UploadConfirmationView, ManualAssign
from cohort_manager.views.pages import LandingView

urlpatterns = [
    re_path(r'api/upload/(?P<upload_id>.*)/',
            UploadConfirmationView.as_view()),
    path('api/upload', UploadView.as_view()),
    path('api/manual_upload', ManualAssign.as_view()),
    re_path(r'^api/collection/(?P<collection_type>.*)/(?P<collection_id>.+)',
            CollectionDetails.as_view()),
    re_path(r'^api/collection/(?P<collection_type>.*)/',
            CollectionList.as_view(),
            name="collection_list"),
    re_path(r'^api/activity/',
            ActivityLog.as_view()),
    re_path(r'^.*$', LandingView.as_view()),
]
