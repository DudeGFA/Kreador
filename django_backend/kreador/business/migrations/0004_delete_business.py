# Generated by Django 4.2 on 2023-05-25 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0018_remove_userexperience_enterprise'),
        ('business', '0003_rename_name_business_business_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Business',
        ),
    ]
