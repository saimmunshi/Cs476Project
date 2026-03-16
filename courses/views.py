from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Feedback, Course, Task
from users.models import CustomUser
from students.models import Student
from teachers.models import Teacher
import cloudinary.uploader


@login_required
def tasks_by_course(request, course_id):

    # Added by Matthew/Spooky: Retrieve all tasks belonging to the specified course.
    tasks = Task.objects.filter(course_id=course_id)

    # Added by Matthew/Spooky: Convert each task into a dictionary so it can be returned as JSON.
    data = [{"id": str(task.id), "title": task.title} for task in tasks]

    # Added by Matthew/Spooky: Return JSON list of tasks to the frontend.
    return JsonResponse(data, safe=False)


@login_required
def feedback_page(request):

    # Added by Matthew/Spooky: Get the currently logged in user.
    user = request.user

    # Added by Matthew/Spooky: Attempt to retrieve the teacher profile associated with the user.
    teacher = Teacher.objects.filter(user=user).first()

    # Added by Matthew/Spooky: If the logged in user is not registered as a teacher show an error and redirect them to the home page.
    if not teacher:
        messages.error(request, "You are not registered as a teacher.")
        return redirect("home")

    # Get all students that share at least one course with this teacher
    #students = Student.objects.filter(
    #    enrolled_courses__teacher=teacher
    #).distinct()

    # Added by Matthew/Spooky: For testing allow teacher to send feedback to any student.
    students = Student.objects.all()

    # Added by Matthew/Spooky: Retrieve all courses that are taught by the current teacher.
    courses = Course.objects.filter(teacher=teacher)

    # Added by Matthew/Spooky: Retrieve feedback received by the teacher and order by newest first.
    received_feedback = Feedback.objects.filter(receiver=user).order_by('-created_at')

    # Added by Matthew/Spooky: Retrieve feedback sent by the teacher and order by newest first.
    sent_feedback = Feedback.objects.filter(sender=user).order_by('-created_at')

    # Added by Matthew/Spooky: Render the feedback page template and pass required data.
    return render(request, "courses/feedback.html", {
        "students": students,
        "courses": courses,
        "received_feedback": received_feedback,
        "sent_feedback": sent_feedback,
    })


@login_required
def send_feedback(request):

    # Added by Matthew/Spooky: Only process the request if its a POST submission.
    if request.method == "POST":

        # Added by Matthew/Spooky: Retrieve data submitted from the feedback form.
        receiver_id = request.POST.get("receiver")
        course_id = request.POST.get("course")
        task_id = request.POST.get("task")
        message = request.POST.get("message")

        # Added by Matthew/Spooky: Validate that a receiver and message were provided.
        if not receiver_id or not message:
            messages.error(request, "Please select a student and write a message.")
            return redirect("courses:feedback_page")

        # Added by Matthew/Spooky: Retrieve the receiver user from the database.
        receiver = CustomUser.objects.get(id=receiver_id)

        # Added by Matthew/Spooky: Retrieve the course if one was selected otherwise set to none.
        course = Course.objects.get(id=course_id) if course_id else None

        # Added by Matthew/Spooky: Retrieve the task if one was selected otherwise set to none.
        task = Task.objects.get(id=task_id) if task_id else None

        # Added by Matthew/Spooky: Default attachment URL is none unless a file is uploaded.
        attachment_url = None

        # Added by Matthew/Spooky: Get uploaded file from the request.
        file = request.FILES.get("attachment")

        # Added by Matthew/Spooky: If a file exists upload it to Cloudinary.
        if file:
            try:
                upload = cloudinary.uploader.upload(file, folder="Mentora_Feedback")
                attachment_url = upload.get("secure_url")
            except Exception as e:
                # Added by Matthew/Spooky: Print upload error to server console.
                print(f"Cloudinary Upload Error: {e}")

                # Added by Matthew/Spooky: Show warning to user if upload fails.
                messages.warning(request, "Attachment upload failed.")

        # Added by Matthew/Spooky: Create a new feedback record in the database.
        Feedback.objects.create(
            sender=request.user,
            receiver=receiver,
            course=course,
            task=task,
            message=message,
            attachment_url=attachment_url
        )

        # Added by Matthew/Spooky: Show success message after feedback is created.
        messages.success(request, "Feedback sent successfully.")

    # Added by Matthew/Spooky: Redirect back to the feedback page after submission.
    return redirect("courses:feedback_page")


@login_required
def edit_feedback(request, feedback_id):

    # Added by Matthew/Spooky: Retrieve the feedback object ensuring it belongs to the current user.
    feedback = get_object_or_404(Feedback, id=feedback_id, sender=request.user)

    # Added by Matthew/Spooky: If the form is submitted update the feedback message.
    if request.method == "POST":

        # Added by Matthew/Spooky: Get the updated message from the form.
        message = request.POST.get("message")

        # Added by Matthew/Spooky: Only update if message is not empty.
        if message:
            feedback.message = message
            feedback.save()

            # Added by Matthew/Spooky: Display success message.
            messages.success(request, "Feedback updated successfully.")

        # Added by Matthew/Spooky: Redirect back to feedback page after editing.
        return redirect("courses:feedback_page")

    # Added by Matthew/Spooky: Render the edit feedback template with existing feedback data.
    return render(request, "courses/edit_feedback.html", {"feedback": feedback})


@login_required
def delete_feedback(request, feedback_id):

    # Added by Matthew/Spooky: Retrieve feedback ensuring the logged in teacher is the sender.
    feedback = get_object_or_404(Feedback, id=feedback_id, sender=request.user)

    # Added by Matthew/Spooky: Only allow deletion if the request method is POST.
    if request.method == "POST":

        # Added by Matthew/Spooky: Delete the feedback from the database.
        feedback.delete()

        # Added by Matthew/Spooky: Notify the user of successful deletion.
        messages.success(request, "Feedback deleted successfully.")

        return redirect("courses:feedback_page")

    # Added by Matthew/Spooky: If request was invalid show an error.
    messages.error(request, "Invalid request.")

    return redirect("courses:feedback_page")


@login_required
def student_feedback(request):

    # Added by Matthew/Spooky: Retrieve all feedback where the current user is the receiver.
    feedback_list = Feedback.objects.filter(receiver=request.user).order_by("-created_at")

    # Added by Matthew/Spooky: Count unread feedback items.
    unread_count = feedback_list.filter(is_read=False).count()

    # Added by Matthew/Spooky: Render the student feedback page with feedback data.
    return render(request, "courses/student_feedback.html", {
        "feedback_list": feedback_list,
        "unread_count": unread_count
    })


@login_required
@require_POST
def mark_feedback_read(request, feedback_id):

    # Added by Matthew/Spooky: Retrieve the feedback ensuring the logged in user is the receiver.
    feedback = get_object_or_404(Feedback, id=feedback_id, receiver=request.user)

    # Added by Matthew/Spooky: Mark feedback as read.
    feedback.is_read = True

    # Added by Matthew/Spooky: Save changes to the database.
    feedback.save()

    # Added by Matthew/Spooky: Return JSON response showing success.
    return JsonResponse({"success": True, "feedback_id": str(feedback.id)})


@login_required
@require_POST
def archive_feedback(request, feedback_id):

    # Added by Matthew/Spooky: Retrieve feedback ensuring the logged in student owns it.
    feedback = get_object_or_404(Feedback, id=feedback_id, receiver=request.user)

    # Added by Matthew/Spooky: Mark feedback as archived for the receiver.
    feedback.is_archived_for_receiver = True

    # Added by Matthew/Spooky: Save changes to the database.
    feedback.save()

    # Added by Matthew/Spooky: Return JSON response showing success.
    return JsonResponse({"success": True, "feedback_id": str(feedback.id)})