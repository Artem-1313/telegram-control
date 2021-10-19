from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance.pk)
    return 'tlg_{0}/{1}'.format(instance.author_id, filename)


class Telegrams(models.Model):
    priority_ = [('1', 'Висока'), ('0', 'Низька')]
    date_create = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    deadline = models.DateTimeField(default=timezone.now)
    tlg_scan = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    tlg_number = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    confirm = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=priority_, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_id(self):
        return str(self.id)


class Executors(models.Model):
    unit = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    telegrams = models.ForeignKey(Telegrams, on_delete=models.CASCADE)
