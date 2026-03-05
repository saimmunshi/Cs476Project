from django.urls import path
from .views import Progress

urlpatterns = [
    path("progress/", Progress, name="teacher-progress"),
]