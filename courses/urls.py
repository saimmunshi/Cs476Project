from django.urls import path
from . import views

# Added by Matthew/Spooky: This list contains all URL routes for this app.
urlpatterns = [

    # Added by Matthew/Spooky: This URL route loads the feedback page where users can view and interact with feedback.
    path(
        "feedback/",
        views.feedback_page,
        name="feedback_page"
    ),

    # Added by Matthew/Spooky: This URL route handles sending feedback from one user to another.
    path(

        # Added by Matthew/Spooky: URL endpoint used when submitting feedback.
        "send-feedback/",

        # Added by Matthew/Spooky: This connects the route to the send_feedback view which processes the feedback submission.
        views.send_feedback,

        # Added by Matthew/Spooky: This name allows the route to be referenced elsewhere in the project such as in templates or redirects.
        name="send_feedback"
    ),

    # Added by Matthew/Spooky: This URL route marks a specific feedback message as read.
    path(

        # Added by Matthew/Spooky: This captures the feedback_id from the URL so the correct feedback item can be updated.
        "feedback/read/<str:feedback_id>/",

        # Added by Matthew/Spooky: This connects the route to the mark_feedback_read view which updates the feedback status.
        views.mark_feedback_read,

        # Added by Matthew/Spooky: This name allows the route to be referenced using djangos URL reversing system.
        name="mark_feedback_read"
    ),

]