from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime

class poll_model(models.Model):
    poll_name = models.CharField(max_length=1000)
    poll_start = models.DateField(default=datetime.now)
    poll_end   = models.DateField()
    eligible = models.ForeignKey(Group)
    vote = models.IntegerField()

class question_model(models.Model):
    poll_name = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    question = models.CharField(max_length=2000)

class answer_model(models.Model):
    question = models.ForeignKey(question_model, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    vote = models.IntegerField()

class history_model(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    