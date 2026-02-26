# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This creates the URL /students/dashboard/
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('feedback/', views.student_feedback_view, name='student_feedback'),
]