from django.urls import path
from . import views  # This only imports from the teachers app

urlpatterns = [
    # If you have teacherHome in teachers/views.py:
    path('home/', views.teacherHome, name='teacher_home'),
    path('courses/', views.teacherCourseList, name='teacher-course-list'),
    path('courses/create-course', views.teacherCreateCourse, name='create-course'),
    
    # Note: This is required for specific course pages
    path('courses/<str:course_id>/', views.teacherCourseMain, name='teacher-course-main'),
]