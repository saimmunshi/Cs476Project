from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField

# Added by Mark: This creates the blueprint for the entire Course and Task system backend.

from users.models import CustomUser

class Feedback(models.Model):
    # Added by Matthew/Spooky: MongoDB primary key.
    id = ObjectIdAutoField(primary_key=True) 

    sender = models.ForeignKey(
        CustomUser,
        related_name="sent_feedbacks",
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        CustomUser,
        related_name="received_feedbacks",
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    task = models.ForeignKey(
        "courses.Task",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    message = models.TextField()
    # Added by Matthew/Spooky: Optional attachment.
    attachment_url = models.URLField(blank=True, null=True)
    # Added by Matthew/Spooky: Track read status.
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    # Added by Matthew/Spooky: Track archived feedback.
    is_archived_for_receiver = models.BooleanField(default=False)

    def __str__(self):
        # Added by Matthew/Spooky: For admin display.
        return f"{self.sender} → {self.receiver}"


class Course(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  title = models.CharField(max_length=200)
  description = models.TextField()
  max_students = models.PositiveIntegerField()

  # Added by Matthew/Spooky: Relations.
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

class Task(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  course = models.ForeignKey(
    Course, 
    on_delete=models.CASCADE, 
    related_name='tasks'
  )
  
  title = models.CharField(max_length=200)
  description = models.TextField()
  start_date = models.DateTimeField(null=True, blank=True)
  due_date = models.DateTimeField(null=True, blank=True)
  points_possible = models.IntegerField(default=100)
  assigned_students = models.ManyToManyField(
      'students.Student',
      related_name='assigned_tasks',
      blank=True
  )
  
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.course.title})"

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
  submission_text = models.TextField(blank=True)
  file_url = models.URLField(blank=True)

  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('reviewed', 'Reviewed'),
  ]
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  
  submitted_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
      # Added by Matthew/Spooky: one submission per student per task.
      unique_together = ('task', 'student')

  def __str__(self):
      return f"Submission: {self.student} - {self.task.title}"

class TaskFeedback(models.Model):
  id = ObjectIdAutoField(primary_key=True)
  
  submission = models.OneToOneField(
      TaskSubmission,
      on_delete=models.CASCADE,
      related_name='feedback'
  )
  grade = models.FloatField()
  # Added by Matthew/Spooky: feedback comments.
  comments = models.TextField(blank=True)
  
  graded_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Feedback for {self.submission}"