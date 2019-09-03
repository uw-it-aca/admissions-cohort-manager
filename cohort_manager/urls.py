from django.urls import path, re_path

from cohort_manager.views.api import UploadView
from cohort_manager.views.pages import LandingView

urlpatterns = [
    path('api/upload', UploadView.as_view()),
    re_path(r'^.*$', LandingView.as_view()),
]
