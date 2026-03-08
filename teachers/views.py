from django.shortcuts import render, redirect
from .models import TaskSubmission

# Added by Matthew/Spooky: Renders the teacher home page.
def teacherHome(request):

    # Added by Matthew/Spooky: This renders the home.html template for the teacher.
    return render(request, 'users/main/templates/home.html')

# Added by Matthew/Spooky: Renders a list of courses for the teacher.
def teacherCourseList(request):

    # Added by Matthew/Spooky: Example list of courses for demonstration purposes.
    courses = ['Math 101', 'CS 476', 'Physics 202']

    # Added by Matthew/Spooky: Renders the course_list.html template passing the list of courses.
    return render(request, 'teachers/course_list.html', {'courses': courses})

# Added by Matthew/Spooky: Renders all task submissions for the teacher to review and provide feedback.
def teacherTaskSubmissions(request):

    # Added by Matthew/Spooky: Retrieves all task submissions from the database.
    submissions = TaskSubmission.objects.all()

    # Added by Matthew/Spooky: Renders the task_submissions.html template with all submissions.
    return render(request, 'teachers/task_submissions.html', {'submissions': submissions})

# Added by Matthew/Spooky: Handles adding teacher feedback to a specific task submission.
def teacherAddFeedback(request, submission_id):

    # Added by Matthew/Spooky: Retrieves the specific submission object from the database by its ID.
    submission = TaskSubmission.objects.get(id=submission_id)

    # Added by Matthew/Spooky: Checks if the form is submitted via POST method.
    if request.method == 'POST':

        # Added by Matthew/Spooky: Retrieves the feedback text submitted by the teacher.
        feedback_text = request.POST.get('feedback', '')

        # Added by Matthew/Spooky: Stores the teacher feedback in the JSONField under the key 'teacher'.
        submission.feedback['teacher'] = feedback_text

        # Added by Matthew/Spooky: Saves the updated submission object back to the database.
        submission.save()

        # Added by Matthew/Spooky: Redirects the teacher back to the task submissions page after saving feedback.
        return redirect('teacher_task_submissions')

    # Added by Matthew/Spooky: Renders the add_feedback.html template passing the submission object.
    return render(request, 'teachers/add_feedback.html', {'submission': submission})