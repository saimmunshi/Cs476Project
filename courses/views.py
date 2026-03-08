from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from users.models import CustomUser
import cloudinary.uploader







# Added by Matthew/Spooky: This view displays the feedback page where users can see feedback they have sent and received.
@login_required
def feedback_page(request):

    # Added by Matthew/Spooky: This stores the currently logged-in user from the request object.
    user = request.user

    # Added by Matthew/Spooky: This retrieves all feedback messages where the logged-in user is the receiver ordered by newest first.
    received = Feedback.objects.filter(receiver=user).order_by('-created_at')

    # Added by Matthew/Spooky: This retrieves all feedback messages where the logged-in user is the sender ordered by newest first.
    sent = Feedback.objects.filter(sender=user).order_by('-created_at')

    # Added by Matthew/Spooky: This renders the feedback.html template and passes both received and sent feedback messages to the template.
    return render(request, "courses/feedback.html", {

        # Added by Matthew/Spooky: Variable used in the template to display feedback received by the user.
        "received_feedback": received,

        # Added by Matthew/Spooky: Variable used in the template to display feedback sent by the user.
        "sent_feedback": sent
    })

# Added by Matthew/Spooky: This view handles the submission of new feedback messages.
@login_required
def send_feedback(request):

    # Added by Matthew/Spooky: This checks that the request is a POST request which indicates that form data was submitted.
    if request.method == "POST":

        # Added by Matthew/Spooky: This retrieves the ID of the user who will receive the feedback from the submitted form data.
        receiver_id = request.POST.get("receiver")

        # Added by Matthew/Spooky: This retrieves the feedback message text from the submitted form.
        message = request.POST.get("message")

        # Added by Matthew/Spooky: This retrieves the receiver user object from the database using the provided ID.
        receiver = CustomUser.objects.get(id=receiver_id)

        # Added by Matthew/Spooky: This initializes the attachment URL variable in case no file is uploaded.
        attachment_url = None

        # Added by Matthew/Spooky: This retrieves the uploaded file from the request if the user attached a file.
        file = request.FILES.get("attachment")

        # Added by Matthew/Spooky: This checks whether a file was uploaded with the feedback.
        if file:
            try:

                # Added by Matthew/Spooky: This uploads the file to cloudinary in the specified folder.
                upload = cloudinary.uploader.upload(

                    # Added by Matthew/Spooky: The file object being uploaded.
                    file,

                    # Added by Matthew/Spooky: The cloudinary folder where the file will be stored.
                    folder="Mentora_Feedback"
                )

                # Added by Matthew/Spooky: This retrieves the secure URL of the uploaded file from cloudinary.
                attachment_url = upload.get("secure_url")

            # Added by Matthew/Spooky: This handles any errors that occur during the cloudinary upload process.
            except Exception as e:

                # Added by Matthew/Spooky: This prints the upload error to the server console for testing.
                print(f"Cloudinary Upload Error: {e}")

        # Added by Matthew/Spooky: This creates a new feedback record in the database with the provided information.
        Feedback.objects.create(

            # Added by Matthew/Spooky: This sets the sender of the feedback as the currently logged-in user.
            sender=request.user,

            # Added by Matthew/Spooky: This sets the receiver of the feedback.
            receiver=receiver,

            # Added by Matthew/Spooky: This stores the message text submitted in the form.
            message=message,

            # Added by Matthew/Spooky: This stores the cloudinary URL if an attachment was uploaded.
            attachment_url=attachment_url
        )

        # Added by Matthew/Spooky: This displays a success message to the user after the feedback has been sent.
        messages.success(request, "Feedback sent successfully.")

    # Added by Matthew/Spooky: This redirects the user back to the feedback page after processing the form.
    return redirect("feedback_page")


# Added by Matthew/Spooky: This view marks a feedback message as read when the receiver opens it.
@login_required
def mark_feedback_read(request, feedback_id):

    # Added by Matthew/Spooky: This retrieves the feedback object from the database using the provided feedback ID.
    feedback = Feedback.objects.get(id=feedback_id)

    # Added by Matthew/Spooky: This checks if the currently logged-in user is the receiver of the feedback.
    if request.user == feedback.receiver:

        # Added by Matthew/Spooky: This updates the feedback record to show it has been read.
        feedback.is_read = True

        # Added by Matthew/Spooky: This saves the updated feedback object to the database.
        feedback.save()

    # Added by Matthew/Spooky: This redirects the user back to the feedback page after marking the message as read.
    return redirect("feedback_page")
