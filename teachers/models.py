from django.db import models
from users.models import MentoraBaseUser
from django_mongodb_backend.fields import ObjectIdAutoField
from users.models import CustomUser

# Added by Matthew/Spooky: The Teacher model extends the MentoraBaseUser to add teacher-specific information.
class Teacher(models.Model):


    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teacher")

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
        return self.user.username
