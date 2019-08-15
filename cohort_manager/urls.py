from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from cohort_manager.views import LandingView, CohortView, LogView, ImportView


urlpatterns = [
    path('', LandingView.as_view()),
    path('log/', LogView.as_view()),
    path('import/', ImportView.as_view()),
    path('cohort/', CohortView.as_view())

]
