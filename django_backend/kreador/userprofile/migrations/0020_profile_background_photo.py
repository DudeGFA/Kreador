# Generated by Django 4.2 on 2023-05-25 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0019_userexperience_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='background_photo',
            field=models.ImageField(default='default.jpg', upload_to='background_photos'),
        ),
    ]
