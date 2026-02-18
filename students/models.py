# students/models.py
from django.db import models
from users.models import MentoraBaseUser
from django_mongodb_backend.fields import ObjectIdAutoField

class Student(MentoraBaseUser):
    id = ObjectIdAutoField(primary_key=True)
    student_id = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'users_student'  # Custom collection name (instead of stupid thing like users_user)
    
    def __str__(self):
        return f"{self.full_name} (Student)"