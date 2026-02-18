# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import ObjectIdAutoField

# 1. The Authentication User
class CustomUser(AbstractUser):
    id = ObjectIdAutoField(primary_key=True)

    def __str__(self):
        return self.username

    # --- ADD THESE PROPERTIES ---
    @property
    def is_student(self):
        """Returns True if the user has a student profile."""
        return hasattr(self, 'students_student_profile')

    @property
    def is_teacher(self):
        """Returns True if the user has a teacher profile."""
        # Note: You will need a Teacher model in a 'teachers' app for this to work
        return hasattr(self, 'teachers_teacher_profile')

# 2. The Abstract Base Class (Shared Blueprint)
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