from django.urls import path
from . import views

# Added by Matthew/Spooky: URL patterns for teacher-specific pages and actions.
urlpatterns = [

    # Added by Matthew/Spooky: Home page for teachers.
    path('home/', views.teacherHome, name='teacher_home'),

    # Added by Matthew/Spooky: Page listing all courses taught by the teacher.
    path('courses/', views.teacherCourseList, name='teacher-course-list'),

    # Added by Matthew/Spooky: Page showing all task submissions for feedback.
    path('submissions/', views.teacherTaskSubmissions, name='teacher_task_submissions'),

    # Added by Matthew/Spooky: Page to add feedback for a specific task submission.
    path('submissions/<str:submission_id>/feedback/', views.teacherAddFeedback, name='teacher_add_feedback'),
]