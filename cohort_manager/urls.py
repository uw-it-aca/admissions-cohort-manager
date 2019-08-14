from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from cohort_manager.views import PageView


urlpatterns = [
    path('', PageView.as_view())
]
