from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    respondedCommentID = models.BigIntegerField()
    deleted = models.BooleanField(default=False)
    #created_at = models.DateTimeField(auto_now_add=True)
