from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PollQuestion(models.Model):
    body = models.CharField(max_length=1000)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    
class PollAnswer(models.Model):
    body = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)
    question_id = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    created = models.DateTimeField()
    updated = models.DateTimeField()

class PollHistory(models.Model):
    question_id = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(PollAnswer,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User)
    created = models.DateTimeField()
    updated = models.DateTimeField()
