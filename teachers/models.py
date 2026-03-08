from django.db import models
from users.models import MentoraBaseUser
from django_mongodb_backend.fields import ObjectIdAutoField

# Added by Matthew/Spooky: The Teacher model extends the MentoraBaseUser to add teacher-specific information.
class Teacher(MentoraBaseUser):

    # Added by Matthew/Spooky: Primary key for the teacher using mongodb ObjectId format.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: Stores the teachers license number.
    license_number = models.CharField(max_length=50)

    # Added by Matthew/Spooky: Stores the teachers area of specialization.
    specialization = models.CharField(max_length=100)

    # Added by Matthew/Spooky: Metadata configuration for the Teacher model.
    class Meta:

        # Added by Matthew/Spooky: This sets the mongodb collection name to 'users_teacher'.
        db_table = 'users_teacher'

    # Added by Matthew/Spooky: Defines how the Teacher object is displayed when printed or in admin.
    def __str__(self):
        return self.username

# Added by Matthew/Spooky: TaskSubmission stores each student's submission for tasks along with teacher feedback.
class TaskSubmission(models.Model):

    # Added by Matthew/Spooky: Primary key for the submission using mongodb ObjectId format.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: Stores the name of the student who submitted the task.
    student_name = models.CharField(max_length=100)

    # Added by Matthew/Spooky: Stores the name of the task being submitted.
    task_name = models.CharField(max_length=100)

    # Added by Matthew/Spooky: JSON field used to store teacher feedback and potentially other structured feedback.
    feedback = models.JSONField(default=dict)

    # Added by Matthew/Spooky: Automatically records the time the submission was created.
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Added by Matthew/Spooky: Defines how the submission object is displayed when printed or in admin.
    def __str__(self):
        return f"{self.student_name} - {self.task_name}"