from django.db import models


class User(models.Model):
    nick = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to = "media")
    authorID = models.BigIntegerField()

class Comment(models.Model):
    imageID = models.BigIntegerField()
    text = models.CharField(max_length=1024)
    userID = models.BigIntegerField()
    respondedCommentID = models.BigIntegerField()