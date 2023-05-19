# Generated by Django 4.1.7 on 2023-04-06 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='company_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Company_name'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
