from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")