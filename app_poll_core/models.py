from django.contrib.auth.models import User
from django.db import models


class poll_model(models.Model):
    poll_name = models.CharField(max_length=1000)
    poll_status = models.CharField(max_length=1)
    poll_start = models.DateField(null=True)
    poll_end = models.DateField(null=True)
    eligible = models.CharField(max_length=100,null=True)
    vote = models.IntegerField(null=True)

class question_model(models.Model):
    poll_name = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    question = models.CharField(max_length=2000)

class answer_model(models.Model):
    question = models.ForeignKey(question_model, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    vote = models.IntegerField(null=True)

class history_model(models.Model):
    user = models.CharField(max_length=100)
    poll = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    
