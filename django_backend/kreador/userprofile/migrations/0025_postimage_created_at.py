# Generated by Django 4.2 on 2023-09-01 22:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0024_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 1, 23, 51, 7, 789179)),
        ),
    ]
