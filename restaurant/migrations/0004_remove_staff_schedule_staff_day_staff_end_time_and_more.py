# Generated by Django 5.0.2 on 2024-03-11 09:37

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_staff_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='schedule',
        ),
        migrations.AddField(
            model_name='staff',
            name='day',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='staff',
            name='end_time',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AddField(
            model_name='staff',
            name='start_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
    ]
