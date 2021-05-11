from django.db import models
from django.contrib.auth.models import User
from django.db.models import Func
from django.contrib.humanize.templatetags import humanize
import hashlib


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=1000, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    flags = models.IntegerField(null=True)

    def get_hash(self):
        return hashlib.md5((self.user.username).encode('utf-8')).hexdigest()

    def get_date(self):
        return humanize.naturaltime(self.createdAt)

    def __str__(self):
        return f"${self.title} ${self.user}"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Dislikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    flags = models.IntegerField(null=True)

    def get_hash(self):
        return hashlib.md5((self.user.username).encode('utf-8')).hexdigest()

    def get_date(self):
        return humanize.naturaltime(self.createdAt)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def get_date(self):
        return humanize.naturaltime(self.createdAt)
