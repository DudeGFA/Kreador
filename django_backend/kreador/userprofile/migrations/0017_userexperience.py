# Generated by Django 4.2 on 2023-05-22 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0016_post_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_name', models.CharField(max_length=50, null=True)),
                ('position', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('enterprise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.business')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
