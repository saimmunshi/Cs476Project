from django.urls import path
from . import views

# Added by Matthew/Spooky: Defines the app namespace so URL names can be referenced as "courses:<name>" in templates and redirects.
app_name = "courses"

# Added by Matthew/Spooky: This list contains all URL routes for this app.
urlpatterns = [

    # Added by Matthew/Spooky: When a user visits "/courses/feedback/" this route calls the feedback_page view.
    path("feedback/",views.feedback_page,name="feedback_page"),

    # Added by Matthew/Spooky: This URL route handles sending feedback from one user to another.
    path("send-feedback/",views.send_feedback,name="send_feedback"),

    # Added by Matthew/Spooky: This loads the student feedback page interface.
    path("student-feedback/",views.student_feedback,name="student_feedback"),

    # Added by Matthew/Spooky: AJAX endpoint used to mark a feedback item as read.
    path("mark-feedback-read/<str:feedback_id>/",views.mark_feedback_read,name="mark_feedback_read"),

    # Added by Matthew/Spooky: API endpoint used by the frontend to retrieve tasks associated with a course.
    path("api/tasks/<str:course_id>/",views.tasks_by_course,name="tasks"),

    # Added by Matthew/Spooky: URL route that allows a teacher to edit feedback they previously sent.
    path("feedback/edit/<str:feedback_id>/",views.edit_feedback,name="edit_feedback"),

    # Added by Matthew/Spooky: URL route that allows a teacher to delete feedback they sent.
    path("feedback/delete/<str:feedback_id>/",views.delete_feedback,name="delete_feedback"),

    # Added by Matthew/Spooky: AJAX endpoint used to archive feedback for the receiving student.
    path("archive-feedback/<str:feedback_id>/",views.archive_feedback,name="archive_feedback"),

]