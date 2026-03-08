from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import ObjectIdAutoField

# Added by Matthew/Spooky: The Course model represents a course created by a teacher.
class Course(models.Model):

    # Added by Matthew/Spooky: Primary key for the course using mongodb's ObjectId format. This uniquely identifies each course in the database.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: Name of the course. CharField is used for strings with a maximum length.
    name = models.CharField(max_length=255)

    # Added by Matthew/Spooky: ForeignKey creates a relationship between this course and the user who teaches it.
    teacher = models.ForeignKey(

        # Added by Matthew/Spooky: This refers to the custom user model defined in settings.py.
        settings.AUTH_USER_MODEL,

        # Added by Matthew/Spooky: If the teacher deletes their account all courses associated with that teacher will also be deleted.
        on_delete=models.CASCADE,

        # Added by Matthew/Spooky: This allows reverse lookup from the user model.
        related_name="courses_taught"
    )

    # Added by Matthew/Spooky: Automatically stores the date and time when the course was first created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Added by Matthew/Spooky: This is used to configure metadata about the model.
    class Meta:

        # Added by Matthew/Spooky: This defines the mongodb collection name for this model.
        db_table = "courses"

    # Added by Matthew/Spooky: This defines how the course object appears when printed in the django admin interface.
    def __str__(self):
        return self.name

# Added by Matthew/Spooky: This represents an activity associated with a specific course.
class Task(models.Model):

    # Added by Matthew/Spooky: Mongodb ObjectId primary key for the task.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: Each task belongs to a specific course.
    course = models.ForeignKey(

        # Added by Matthew/Spooky: Reference to the Course model.
        Course,

        # Added by Matthew/Spooky: If a course is deleted, all tasks associated with that course will also be deleted.
        on_delete=models.CASCADE,

        # Added by Matthew/Spooky: This enables reverse lookup.
        related_name="tasks"
    )

    # Added by Matthew/Spooky: Title of the task.
    title = models.CharField(max_length=255)

    # Added by Matthew/Spooky: Detailed description of the task. TextField is used instead of CharField because descriptions can be much longer.
    description = models.TextField()

    # Added by Matthew/Spooky: Automatically records the time the task was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Added by Matthew/Spooky: Meta configuration for this model.
    class Meta:

        # Added by Matthew/Spooky: This specifies the mongodb collection name.
        db_table = "tasks"

    # Added by Matthew/Spooky: Controls how the task object is displayed when printed in the admin panel.
    def __str__(self):
        return self.title

# Added by Matthew/Spooky: This stores a students response to a task.
class TaskSubmission(models.Model):

    # Added by Matthew/Spooky: Primary key for the submission using mongodb ObjectId.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: This links the submission to the task being completed.
    task = models.ForeignKey(

        # Added by Matthew/Spooky: Reference to the task model.
        Task,

        # Added by Matthew/Spooky: If the task is deleted all submissions associated to that task will also be deleted.
        on_delete=models.CASCADE
    )

    # Added by Matthew/Spooky: This links the submission to the student who submitted it.
    student = models.ForeignKey(

        # Added by Matthew/Spooky: Uses the project's custom user model.
        settings.AUTH_USER_MODEL,

        # Added by Matthew/Spooky: If the student account is deleted their submissions will also be deleted.
        on_delete=models.CASCADE
    )

    # Added by Matthew/Spooky: This stores the response submitted by the student.
    submission_text = models.TextField()

    # Added by Matthew/Spooky: This automatically records the time the submission was made.
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Added by Matthew/Spooky: Metadata for the model.
    class Meta:

        # Added by Matthew/Spooky: This defines the mongodb collection name.
        db_table = "task_submissions"

# Added by Matthew/Spooky: The Feedback model allows users to send feedback messages to one another like from teacher to student.
class Feedback(models.Model):

    # Added by Matthew/Spooky: Mongodb ObjectId primary key for the feedback record.
    id = ObjectIdAutoField(primary_key=True)

    # Added by Matthew/Spooky: The user who sends the feedback message.
    sender = models.ForeignKey(

        # Added by Matthew/Spooky: References the custom user model.
        settings.AUTH_USER_MODEL,

        # Added by Matthew/Spooky: If the sender account is deleted their sent feedback messages are also deleted.
        on_delete=models.CASCADE,

        # Added by Matthew/Spooky: Allows reverse queries.
        related_name="feedback_sent"
    )

    # Added by Matthew/Spooky: The user receiving the feedback message.
    receiver = models.ForeignKey(

        # Added by Matthew/Spooky: References the custom user model.
        settings.AUTH_USER_MODEL,

        # Added by Matthew/Spooky: If the receiver account is deleted the feedback messages sent to them are also deleted.
        on_delete=models.CASCADE,

        # Added by Matthew/Spooky: Allows reverse queries.
        related_name="feedback_received"
    )

    # Added by Matthew/Spooky: This stores the text of the feedback message.
    message = models.TextField()

    # Added by Matthew/Spooky: Optional URL for attachments.
    attachment_url = models.URLField(

        # Added by Matthew/Spooky: Maximum length allowed for the URL.
        max_length=500,

        # Added by Matthew/Spooky: Allows the field to be NULL in the database.
        null=True,

        # Added by Matthew/Spooky: Allows the field to be left empty in forms.
        blank=True
    )

    # Added by Matthew/Spooky: Boolean flag used to track whether the receiver has read the feedback message.
    is_read = models.BooleanField(default=False)

    # Added by Matthew/Spooky: Timestamp showing when the feedback message was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Added by Matthew/Spooky: Metadata configuration for the model.
    class Meta:

        # Added by Matthew/Spooky: Defines the mongodb collection name.
        db_table = "feedback"

    # Added by Matthew/Spooky: Defines the string representation of the feedback object for debugging and admin display.
    def __str__(self):

        # Added by Matthew/Spooky: Displays sender → receiver format.
        return f"{self.sender} → {self.receiver}"