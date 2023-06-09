# Generated by Django 4.0.3 on 2023-06-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_category_ad_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='responders',
            field=models.ManyToManyField(blank=True, null=True, to='main.respond'),
        ),
    ]
