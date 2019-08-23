from django.urls import path, include

urlpatterns = [
    path('', include('cohort_manager.urls'))
]
