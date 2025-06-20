from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=user_directory_path, default='default.jpg')

class Chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    message=models.TextField()
    response=models.TextField()
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}:{self.message}'
    