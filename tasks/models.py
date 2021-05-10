from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


class Task(models.Model):
    """ Task model class """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Task name', max_length=200)
    description = models.CharField(verbose_name='Description', max_length=2000, blank=True)
    type = models.IntegerField('Event or Task', choices=((0, "Event"), (1, "Task")))
    created = models.DateTimeField(verbose_name='Creation date time', auto_now=True)
    deadline = models.DateTimeField(verbose_name='Task deadline')
    complete = models.BooleanField(verbose_name='Complete', default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "Task: " + self.name
