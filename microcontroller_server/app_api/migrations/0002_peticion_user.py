# Generated by Django 5.0 on 2024-01-11 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='peticion',
            name='user',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
