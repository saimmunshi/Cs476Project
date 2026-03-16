from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Added by Matthew/Spooky: Add any extra fields common to both students and teachers here.
    pass

class MentoraBaseUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True