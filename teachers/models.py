from django.db import models
from users.models import MentoraBaseUser
from django_mongodb_backend.fields import ObjectIdAutoField

class Teacher(MentoraBaseUser):
    id = ObjectIdAutoField(primary_key=True)
    student_id = models.CharField(max_length=50)
    
    # This MUST be indented exactly like the fields above
    class Meta:
        db_table = 'users_teacher'
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['user']),
        ]
"""class Teacher(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="teacher_profile"
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    license_number = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    profile_image_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'teachers_teacher'

    def __str__(self):
        return self.full_name

"""
