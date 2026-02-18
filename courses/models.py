# courses/models.py
from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField

# Class: Course (collection = courses_course)
# 
#
#
class Course(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  title = models.CharField(max_length=200)
  description = models.TextField()
  
  # RELATIONS
  teacher = models.ForeignKey(
    'teachers.Teacher', 
    on_delete=models.CASCADE,
    related_name='courses'
  )
  students = models.ManyToManyField(
    'students.Student',
    related_name='enrolled_courses',
    blank=True
  )
  
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

# Class: Task (collection = courses_task)
# 
#
#
class Task(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  course = models.ForeignKey(
    Course, 
    on_delete=models.CASCADE, 
    related_name='tasks'
  )
  
  title = models.CharField(max_length=200)
  description = models.TextField()
  start_date = due_date = models.DateTimeField(null=True, blank=True)
  due_date = models.DateTimeField(null=True, blank=True)
  points_possible = models.IntegerField(default=100) # e.g., Out of 100
  
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.course.title})"

# Class: TaskSubmission (collection = courses_tasksubmission)
# Goal: Represents the student's actual work (the file or answer).
#
#
class TaskSubmission(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  
  task = models.ForeignKey(
      Task, 
      on_delete=models.CASCADE,
      related_name='submissions'
  )
  student = models.ForeignKey(
      'students.Student', 
      on_delete=models.CASCADE,
      related_name='submissions'
  )
  
  # The content of the submission
  submission_text = models.TextField(blank=True) 
  file_url = models.URLField(blank=True) # If they upload a file
  
  submitted_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
      # Ensures a student can only submit ONCE per task
      # If they submit again, they should update this existing record
      unique_together = ('task', 'student')

  def __str__(self):
      return f"Submission: {self.student} - {self.task.title}"

# Class: TaskFeedBack (collection = courses_taskfeedback)
# 
#
#
class TaskFeedback(models.Model):
  """
  Represents the teacher's grading and comments.
  """
  id = ObjectIdAutoField(primary_key=True)
  
  # OneToOne because one submission has exactly one feedback/grade
  submission = models.OneToOneField(
      TaskSubmission,
      on_delete=models.CASCADE,
      related_name='feedback' # Access via: submission.feedback
  )
  
  grade = models.FloatField() # e.g., 95.5
  comments = models.TextField(blank=True) # "Great job, but check spelling."
  
  graded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"Feedback for {self.submission}"