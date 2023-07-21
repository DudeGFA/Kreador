# Generated by Django 4.2 on 2023-05-24 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_remove_business_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='name',
            new_name='business_name',
        ),
        migrations.AlterField(
            model_name='business',
            name='city',
            field=models.CharField(default='Ibadan', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='business',
            name='country',
            field=models.CharField(default='Nigeria', max_length=30),
            preserve_default=False,
        ),
    ]
