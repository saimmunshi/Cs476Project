from django.shortcuts import render


# Create your views here.
# Note from Mark: This page will have to be very much changed to be in line with students/views.py

"""
Name Function: Home
type: Function 
Purpose: Connects to the Teacher Home dashboard
"""
def Home(request):  
    # Looks in teachers/features/Home/templates/Home/Home.html
    return render(request, 'Home/Home.html')

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
    return render(request, 'My_Student/My_Student.html')

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


#added by win516
"""
Name Function: Progress
type: Function
Purpose: Connects to the Teacher Progress dashboard feature
"""

def Progress(request):
    # Mock data (safe to use before DB integration)
    students = [
        {"name": "Ali Khan", "progress": 85, "pending": 1},
        {"name": "Sara Ahmed", "progress": 60, "pending": 3},
        {"name": "John Smith", "progress": 40, "pending": 5},
    ]

    stats = {
        "total_students": len(students),
        "avg_progress": round(sum(s["progress"] for s in students) / len(students)),
        "needs_attention": sum(1 for s in students if s["progress"] < 50 or s["pending"] >= 3),
    }

    # Looks in teachers/features/Progress/templates/progress.html
    return render(request, "Progress/templates/progress.html", {
        "students": students,
        "stats": stats,
    })