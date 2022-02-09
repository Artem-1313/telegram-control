# Generated by Django 3.2.11 on 2022-01-29 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='telegramsControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=200)),
                ('unit_to_report', models.CharField(max_length=100, null=True, verbose_name='Кому доповісти:')),
                ('tlg_number', models.CharField(max_length=100, null=True, verbose_name='Номер вихідної телеграми')),
                ('description', models.TextField(verbose_name='Опис телеграми')),
                ('priority', models.CharField(blank=True, choices=[('1', 'Висока'), ('0', 'Низька')], default=0, max_length=20, verbose_name='Важливість телеграми')),
                ('tlg_scan', models.FileField(blank=True, null=True, upload_to='tlg_storage', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Завантажити скан-копію телеграми')),
            ],
        ),
    ]
