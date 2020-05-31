from django.db import models
from django.contrib.auth.models import User

# USER PROFILE PHOTO
class ProfilePhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return "{}'s Profile photo".format(self.user.username)