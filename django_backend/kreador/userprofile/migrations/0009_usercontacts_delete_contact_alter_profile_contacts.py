# Generated by Django 4.2 on 2023-04-23 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0008_contact_remove_profile_users_following_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usercontacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userprofile.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('profile', 'user')},
            },
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.AlterField(
            model_name='profile',
            name='contacts',
            field=models.ManyToManyField(blank=True, related_name='contacted_by', through='userprofile.Usercontacts', to=settings.AUTH_USER_MODEL),
        ),
    ]
