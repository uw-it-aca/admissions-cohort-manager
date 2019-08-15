from django.urls import path, re_path
from cohort_manager.views import LandingView, CohortView, LogView, ImportView


urlpatterns = [
    path('', LandingView.as_view()),
    path('log/', LogView.as_view()),
    path('import/', ImportView.as_view()),
    re_path(r'cohort/(?P<cohort_code>\d+)', CohortView.as_view())
]
