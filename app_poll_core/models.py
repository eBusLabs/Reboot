from django.db import models


class poll_model(models.Model):
    poll_name = models.CharField(max_length=1000)
    poll_start = models.DateField(null=True)
    poll_end = models.DateField(null=True)
    group = models.CharField(max_length=100,null=True)
    created_by = models.CharField(max_length=8)
    total_vote = models.IntegerField(null=True)
    
    def __str__(self):
        return self.poll_name

class question_model(models.Model):
    poll_name = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    question = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.question

class answer_model(models.Model):
    question = models.ForeignKey(question_model, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    vote = models.IntegerField(null=True)
    
    def __str__(self):
        return self.option

class history_model(models.Model):
    user = models.CharField(max_length=100)
    poll = models.ForeignKey(poll_model, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    
