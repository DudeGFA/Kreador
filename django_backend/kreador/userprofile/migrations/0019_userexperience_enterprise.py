# Generated by Django 4.2 on 2023-05-25 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_initial'),
        ('userprofile', '0018_remove_userexperience_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexperience',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.business'),
        ),
    ]
