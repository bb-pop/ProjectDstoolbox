from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email uniqueness
    profile_picture = models.URLField(null=True, blank=True)  # Allow for no profile picture
    #Use StudentID instead of id for the primary key
    StudentID = models.CharField(max_length=11, primary_key=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name