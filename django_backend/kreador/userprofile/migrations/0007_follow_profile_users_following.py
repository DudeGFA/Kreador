# Generated by Django 4.2 on 2023-04-20 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_remove_post_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userprofile.profile')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usersfollowing', to='userprofile.profile')),
            ],
            options={
                'unique_together': {('following', 'followers')},
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='users_following',
            field=models.ManyToManyField(blank=True, related_name='users_followers', through='userprofile.Follow', to='userprofile.profile'),
        ),
    ]
