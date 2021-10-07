from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Telegrams(models.Model):
    priority_ = [('1', 'Висока'), ('0', 'Низька')]
    date_create = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    deadline = models.DateTimeField(default=timezone.now)
    tlg_scan = models.FileField(upload_to='tlg_dir/', null=True, blank=True)
    tlg_number = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    confirm = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=priority_, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Executors(models.Model):
    unit = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    telegrams = models.ForeignKey(Telegrams, on_delete=models.CASCADE)
