# Generated by Django 4.2 on 2023-06-09 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_profile_background_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background_photo',
            field=models.ImageField(default='background_photos/default.jpg', upload_to='background_photos'),
        ),
    ]
