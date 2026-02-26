from django.shortcuts import render

from django.shortcuts import render #added by win516
from datetime import date, timedelta #added by win516

# Create your views here.

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



# added by win516
"""
Name Function: Mentor_Progress_Dashboard
type: Function
Purpose: Shows mentor overview of student progress and attention needed
"""

def mentor_progress_dashboard(request):
    raw_students = [
        {"name": "Alex Johnson", "course": "Python Fundamentals", "progress": 72, "overdue": 0, "last_activity": date.today() - timedelta(days=1)},
        {"name": "Maya Singh", "course": "Web Dev Basics", "progress": 38, "overdue": 2, "last_activity": date.today() - timedelta(days=2)},
        {"name": "Chris Lee", "course": "Data Structures", "progress": 55, "overdue": 0, "last_activity": date.today() - timedelta(days=10)},
        {"name": "Samira Ahmed", "course": "Intro to Databases", "progress": 90, "overdue": 0, "last_activity": date.today()},
        {"name": "Jordan Park", "course": "Python Fundamentals", "progress": 22, "overdue": 1, "last_activity": date.today() - timedelta(days=12)},
    ]

    students = []
    attention = []
    total_progress = 0

    for s in raw_students:
        days_inactive = (date.today() - s["last_activity"]).days

        if days_inactive >= 7:
            status = "inactive"
        elif s["overdue"] > 0 or s["progress"] < 40:
            status = "behind"
        else:
            status = "ontrack"

        total_progress += s["progress"]

        students.append({
            "name": s["name"],
            "course": s["course"],
            "progress": s["progress"],
            "overdue": s["overdue"],
            "last_activity": s["last_activity"].isoformat(),
            "status": status,
        })

        if status == "inactive":
            attention.append({"name": s["name"], "reason": f"Inactive for {days_inactive} days.", "badge": "inactive"})
        elif status == "behind":
            reason = f"{s['overdue']} overdue task(s)." if s["overdue"] > 0 else "Progress below 40%."
            attention.append({"name": s["name"], "reason": reason, "badge": "behind"})

    selected_course = request.GET.get("course", "").strip()
    selected_student = request.GET.get("student", "").strip()
    selected_status = request.GET.get("status", "").strip()

    filtered = students
    if selected_course:
        filtered = [x for x in filtered if x["course"] == selected_course]
    if selected_student:
        filtered = [x for x in filtered if x["name"] == selected_student]
    if selected_status:
        filtered = [x for x in filtered if x["status"] == selected_status]

    courses = sorted({s["course"] for s in students})
    student_names = sorted({s["name"] for s in students})

    avg_progress = round(total_progress / len(students)) if students else 0
    stats = {
        "active_students": len(students),
        "avg_progress": avg_progress,
        "needs_attention": len(attention),
    }

    return render(request, "mentor/progress_dashboard.html", {
        "stats": stats,
        "students": filtered,
        "attention": attention[:5],
        "courses": courses,
        "student_names": student_names,
        "selected": {"course": selected_course, "student": selected_student, "status": selected_status},
    })
