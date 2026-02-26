#added by win516
from django.urls import path
from .views import mentor_progress_dashboard

urlpatterns = [
    path("dashboard/progress/", mentor_progress_dashboard, name="mentor_progress_dashboard"),
]
