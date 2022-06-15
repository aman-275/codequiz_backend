from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Question(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name="questions", on_delete=models.CASCADE)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    answer = models.TextField()
    correct = models.BooleanField(default=False)


class Comment(models.Model):
    question = models.ForeignKey(
        Question, related_name="comments", on_delete=models.CASCADE
    )
    comment = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
