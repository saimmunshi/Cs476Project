from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from courses.models import Course, Task, TaskSubmission
import cloudinary.uploader  # For task submission

# Create your views here.
"""
Name Function: Home
type: Function 
Purpose:It is used connect django with home html file through an http request

"""
def studentHome(request):  
    return render(request, 'StudentHomePage/templates/StudentHomePage.html')
"""
Name Function: Calender
type: Function 
Purpose:It is used connect django with Calender html file through an http request

"""
def Calender(request):  
    return render(request, '\Home\templates\Calender.html')

"""
Name Function: Mentor
type: Function 
Purpose:It is used connect django with Calender Mentor file through an http request

"""
def Mentor(request):  
    return render(request, '\Mentors\templates\Mentor.html')


"""
Name Function: Skills
type: Function 
Purpose:It is used connect django with Calender Skills file through an http request

"""
def Progress(request):  
    return render(request, '\Progess\templates\Progess.html')


"""
Student Courses Views and Functions:
- Mark: Below are all the Course related functionality on the student's side
"""
# Helper function to check auth and get the student profile
def get_student_profile(user):
    if not getattr(user, 'is_student', False):
        return None
    try:
        # Assuming this is your related name based on previous examples
        return user.students_student_profile 
    except AttributeError:
        return None

@login_required
def courseBrowser(request):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    courses = Course.objects.all()
    context = {
        'courses': courses,
        'student': student  # Passing student so we can check if they already joined a course
    }
    # Note: Update template path if needed based on your folder structure
    return render(request, 'Courses/templates/course-browser.html', context)

@login_required
def joinCourse(request, course_id):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        
        # Check if course is not full
        if course.students.count() < course.max_students:
            course.students.add(student) # Adds the student to the ManyToMany field!
        
        return redirect('my-courses')
    
    return HttpResponseBadRequest("Invalid Request")

@login_required
def myCourses(request):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    # Only get courses where THIS student is in the 'students' ManyToMany list
    courses = student.enrolled_courses.all()
    
    context = {'courses': courses}
    return render(request, 'Courses/templates/my-courses.html', context)

@login_required
def studentCourseMain(request, course_id):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    # get_object_or_404 ensures the student is actually enrolled in this specific course!
    course = get_object_or_404(Course, id=course_id, students=student)
    
    context = {'course': course}
    return render(request, 'Courses/templates/student-course-main.html', context)

@login_required
def leaveCourse(request, course_id):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    if request.method == "POST":
        # get_object_or_404 with students=student ensures they can only leave a course they are actually in
        course = get_object_or_404(Course, id=course_id, students=student)
        
        # Remove the student from the ManyToMany list
        course.students.remove(student) 
        
        # Redirect back to their course list
        return redirect('my-courses')
    
    return HttpResponseBadRequest("Invalid Request")

"""
Task Pages
"""
@login_required
def studentTasks(request):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    # 1. Get all tasks specifically assigned to this student
    tasks = Task.objects.filter(assigned_students=student).order_by('due_date')

    # 2. Package the tasks with their submission status so the HTML can display "Pending" vs "Submitted"
    task_data = []
    for t in tasks:
        # Check if a submission already exists for this task + student combination
        submission = TaskSubmission.objects.filter(task=t, student=student).first()
        task_data.append({
            'task': t,
            'status': submission.status if submission else 'Not Submitted',
            'is_submitted': bool(submission)
        })

    context = {'task_data': task_data}
    return render(request, 'tasks/templates/student-tasks.html', context)

@login_required
def studentTaskSubmit(request, task_id):
    student = get_student_profile(request.user)
    if not student:
        return HttpResponseForbidden("You must be logged in as a student.")

    task = get_object_or_404(Task, id=task_id, assigned_students=student)
    submission = TaskSubmission.objects.filter(task=task, student=student).first()

    if request.method == "POST":
        submission_text = request.POST.get('submission_text', '')
        media_file = request.FILES.get('attached_file')
        
        # Keep the existing URL unless they upload a new file
        uploaded_file_url = submission.file_url if submission else ""

        # Cloudinary Upload Logic matches your registration view!
        if media_file:
            try:
                # resource_type="auto" is REQUIRED for Cloudinary to accept videos!
                upload_result = cloudinary.uploader.upload(
                    media_file, 
                    folder="submission_files",
                    resource_type="auto" 
                )
                uploaded_file_url = upload_result.get('secure_url')
                print(f"Task Submit: Cloudinary Success: {uploaded_file_url}")
            except Exception as e:
                print(f"Task Submit: Cloudinary Error: {e}")
                # Optional: you could use messages.error here to tell the user it failed

        if submission:
            # Update existing submission
            submission.submission_text = submission_text
            if uploaded_file_url: 
                submission.file_url = uploaded_file_url
            submission.save()
        else:
            # Create a brand new submission
            TaskSubmission.objects.create(
                task=task,
                student=student,
                submission_text=submission_text,
                file_url=uploaded_file_url,  # Save the secure_url string!
                status='pending'
            )
        
        return redirect('student-tasks')

    context = {
        'task': task,
        'submission': submission
    }
    return render(request, 'tasks/templates/student-task-submit.html', context)