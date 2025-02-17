from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True )
    is_google_user = models.BooleanField(default=False)
    # is_facebook_user = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    
User = get_user_model()

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"