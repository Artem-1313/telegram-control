from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Telegrams(models.Model):
    date_create = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Executors(models.Model):
    unit = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    telegrams = models.ForeignKey(Telegrams, on_delete=models.CASCADE)