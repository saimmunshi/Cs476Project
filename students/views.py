# students/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Requires login and checks if the user is a student.
@login_required
def student_dashboard_view(request):
    if not request.user.is_student:
        # Note from Mark: I'd like to make an "Oops!" sort of page. I'll probably do this on my own once we have an established visual identity.
        return HttpResponseForbidden("You are not authorized to view the student dashboard. Please log in with a student account.")

    student_profile = request.user.students_student_profile
    context = {
        'student': student_profile
    }
    return render(request, 'dashboard/templates/dashboard.html', context)

# Requires login and checks if the user is a student.
@login_required
def student_feedback_view(request):
    if not request.user.is_student:
        return HttpResponseForbidden("You are not authorized to view the student feedback page. Please log in with a student account.")

    student_profile = request.user.students_student_profile
    context = {
        'student': student_profile
    }
    return render(request, 'feedback/templates/feedback.html', context)

# Changed by Mark: Changed the view function names to be lower case and added suffix "_view" for consistency

# Purpose: Used connect Django with Calender .html file through an HTTP request
def calendar_view(request):
    return render(request, 'Calender/templates/Calender.html')

def mentors_view(request):
    return render(request, 'Mentors/templates/Mentor.html')

def skills_view(request):
    return render(request, 'Skills/templates/Skills.html')

def tasks_view(request):
    return render(request, 'features/Tasks/Tasks.html')