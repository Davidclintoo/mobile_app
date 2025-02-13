from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True )
    
    def __str__(self):
        return self.username
