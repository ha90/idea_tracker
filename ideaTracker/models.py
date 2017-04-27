from django.db import models

# Create your models here.
class Idea(models.Model):
    priority = models.IntegerField()
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=500)

