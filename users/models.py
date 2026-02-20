# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import ObjectIdAutoField

# Authentication User
class CustomUser(AbstractUser):
    id = ObjectIdAutoField(primary_key=True)

    def __str__(self):
        return self.username

    @property
    def is_student(self):
        # Returns true if the user has a student profile.
        return hasattr(self, 'students_student_profile')

    @property
    def is_teacher(self):
        # Returns true if the user has a teacher profile.
        return hasattr(self, 'teachers_teacher_profile')

# Abstract Base Class (Parent class for Student and Teacher model)
# See teachers/models.py or students/models.py
class MentoraBaseUser(models.Model):
    # We reference the CustomUser via settings to avoid circular imports
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_profile"
    )
    full_name = models.CharField(max_length=255)
    profile_image_url = models.URLField(max_length=500, null=True, blank=True)
    
    class Meta:
        abstract = True