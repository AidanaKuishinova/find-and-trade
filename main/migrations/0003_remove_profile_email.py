# Generated by Django 4.1.7 on 2023-04-03 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
