from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class User(AbstractUser):
    followers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='followings'
    )
    myinfo = models.TextField(blank=True, null=True)
    image = ProcessedImageField(upload_to='',processors=[ResizeToFill(100,100)],blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)