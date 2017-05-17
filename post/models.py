from django.db import models
from library.models import Topic, Spec
from account.models import MyUser

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic)
    spec = models.ForeignKey(Spec)
    title = models.CharField(max_length=255, unique=False)
    created = models.TimeField(auto_now_add=True)
    changed = models.TimeField(auto_now=True)
    publisher = models.ForeignKey(MyUser)
    viewed = models.IntegerField(default=0)

class PostPhoto(models.Model):
    post = models.ForeignKey(Post)
    picture = models.CharField(max_length=255, unique=False)
    thumb = models.CharField(max_length=255, unique=False)

class PostVideo(models.Model):
    post = models.ForeignKey(Post)
    data = models.CharField(max_length=255, unique=False)
    preview = models.CharField(max_length=255, unique=False)
