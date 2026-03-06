from django.urls import path
from . import views  # This only imports from the teachers app

urlpatterns = [
    path('home/', views.teacherHome, name='teacher_home'),

    # Note by Mark: Uncomment these once views are merged from main
    # path('courses/', views.teacherCourseList, name='teacher-course-list'),
    # path('courses/create-course', views.teacherCreateCourse, name='create-course'),
    # path('courses/<str:course_id>/', views.teacherCourseMain, name='teacher-course-main'),
    # path('create-task/', views.Create_Task, name='create-task'),
    # path('tasks/<str:task_id>/submissions/', views.teacherTaskSubmissions, name='teacher-task-submissions'),
    # path('submissions/<str:submission_id>/feedback/', views.teacherFeedback, name='teacher-feedback'),

    # Added by win516
    path('progress/', views.Progress, name='teacher_progress'),
]