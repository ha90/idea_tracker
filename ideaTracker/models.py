from django.db import models

# Create your models here.
class Idea(models.Model):
    priority = models.IntegerField(default=9)
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=500)
    status = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
