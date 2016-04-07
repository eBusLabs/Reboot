from django.db import models


class poll_model(models.Model):
    poll_name = models.CharField(max_length=1000)
    poll_start = models.DateField(null=True, db_index=True)
    poll_end = models.DateField(null=True, db_index=True)
    created_by = models.CharField(max_length=8)
    total_vote = models.IntegerField(default=0)
    
    def __str__(self):
        return self.poll_name

class poll_group_model(models.Model):
    poll_group = models.CharField(max_length=80)
    poll_name = models.ForeignKey(poll_model,on_delete=models.CASCADE, db_index=True)
    
    def __str__(self):
        return self.poll_group

class question_model(models.Model):
    poll_name = models.ForeignKey(poll_model, on_delete=models.CASCADE, db_index=True)
    question = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.question

class answer_model(models.Model):
    question = models.ForeignKey(question_model, on_delete=models.CASCADE, db_index=True)
    option = models.CharField(max_length=500)
    vote = models.IntegerField(default=0)
    
    def __str__(self):
        return self.option

class history_model(models.Model):
    user = models.IntegerField()
    poll_name = models.ForeignKey(poll_model, on_delete=models.CASCADE, db_index=True)
    taken = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.taken)
    
