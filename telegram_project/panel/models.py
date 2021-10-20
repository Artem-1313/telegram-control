import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


# Create your models here.


def user_directory_path(instance, filename):
    current_day = date.today()
    ext = filename.split('.')[-1]
    filename = f"{str(uuid.uuid4().hex)}.{ext}"
    return f'tlg_dir/{instance.author_id}/{current_day.year}/{current_day.month}/{filename}'


class Telegrams(models.Model):
    priority_ = [('1', 'Висока'), ('0', 'Низька')]
    date_create = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    deadline = models.DateTimeField(default=timezone.now)
    tlg_scan = models.FileField(upload_to=user_directory_path, null=True, blank=True,
                                validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    tlg_number = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    confirm = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=priority_, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_id(self):
        return str(self.id)

    def replace_tlg_pdf(self):
        return str(self.tlg_scan)


class Executors(models.Model):
    unit = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    telegrams = models.ForeignKey(Telegrams, on_delete=models.CASCADE)


@receiver(pre_delete, sender=Telegrams)
def Telegrams_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.tlg_scan.delete(False)
