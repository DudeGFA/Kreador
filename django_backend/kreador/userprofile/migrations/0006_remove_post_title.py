# Generated by Django 4.2 on 2023-04-19 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_reply_rename_like_postlike_replylike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
