from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course   # Import the Course model
from teachers.models import Teacher # Import the Teacher model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
#from django.contrib.auth.decorators import login_required

# Create your views here.

#@login_required


"""
Name Function: Home
type: Function 
Purpose: Connects to the Teacher Home dashboard
"""
def teacherHome(request):  
    # Looks in teachers/features/Home/templates/Home/Home.html
    return render(request, 'TeacherHomePage/templates/TeacherHomePage.html')


"""
Added by Mark: Course List page
"""
@login_required
def teacherCourseList(request):  
    if not getattr(request.user, 'is_teacher', False):
        return HttpResponseForbidden("You are not authorized. Please log in with a teacher account.")

    try:
        current_teacher = request.user.teachers_teacher_profile
    except AttributeError:
        return HttpResponseForbidden("Teacher profile not found.")

    # 1. Grab all courses created by this specific teacher
    courses = Course.objects.filter(teacher=current_teacher)

    # 2. Pass those courses to the HTML template in a context dictionary
    context = {
        'courses': courses
    }
    return render(request, 'teacher-courses/templates/teacher-course-list.html', context)


"""
Added by Mark: Create Course
"""
@login_required
def teacherCreateCourse(request):  
    # 1. Make sure the user is actually a teacher (matching your student example)
    if not getattr(request.user, 'is_teacher', False):
        return HttpResponseForbidden("You are not authorized to create courses. Please log in with a teacher account.")

    # 2. Get the teacher profile using the same pattern as your student view
    try:
        # NOTE: If your users/models.py uses a different related name (like 'teacher_profile'), change it here!
        # I am guessing it is 'teachers_teacher_profile' based on your student example.
        current_teacher = request.user.teachers_teacher_profile 
    except AttributeError:
        # If the profile doesn't exist, stop them safely instead of crashing
        return HttpResponseForbidden("Teacher profile not found for this user. Please contact support.")

    # 3. Handle the form submission
    if request.method == "POST":
        course_title = request.POST.get('title')
        course_description = request.POST.get('description')
        max_students = request.POST.get('max_students')

        # Save the course to MongoDB
        Course.objects.create(
            title=course_title,
            description=course_description,
            max_students=max_students,
            teacher=current_teacher
        )

        # Redirect back to the course list
        return redirect('teacher-course-list')

    # 4. If it's just a GET request, render the empty form
    return render(request, 'teacher-courses/templates/create-course.html')

"""
Added by Mark: Create Course
"""
@login_required
def teacherCourseMain(request, course_id):
    if not getattr(request.user, 'is_teacher', False):
        return HttpResponseForbidden("You are not authorized.")

    try:
        current_teacher = request.user.teachers_teacher_profile
    except AttributeError:
        return HttpResponseForbidden("Teacher profile not found.")

    # 1. Get the specific course by ID. 
    # We also pass teacher=current_teacher to ensure they can't view another teacher's course!
    course = get_object_or_404(Course, id=course_id, teacher=current_teacher)

    # 2. Pass the single course to the HTML template
    context = {
        'course': course
    }
    return render(request, 'teacher-courses/templates/teacher-course-main.html', context)

"""
Name Function: Calendar
type: Function 
Purpose: Connects to the Teacher Calendar feature
"""
def Calendar(request):  
    # Looks in teachers/features/Calendar/templates/Calendar/Calendar.html
    return render(request, 'Calendar/Calendar.html')

"""
Name Function: My_Student
type: Function 
Purpose: Connects to the My Student management feature
"""
def My_Student(request):  
    # Looks in teachers/features/My_Student/templates/My_Student/My_Student.html
    return render(request, 'My_Student/templates/My_Student.html')

"""
Name Function: Create_Task
type: Function 
Purpose: Connects to the Task creation feature
"""
def Create_Task(request):  
    # Looks in teachers/features/Create_Task/templates/Create_Task/Create_Task.html
    return render(request, 'Create_Task/Create_Task.html')

"""
Name Function: Meeting
type: Function 
Purpose: Connects to the Meeting/Video call feature
"""
def Meeting(request):  
    # Looks in teachers/features/Meeting/templates/Meeting/Meeting.html
    return render(request, 'Meeting/Meeting.html')