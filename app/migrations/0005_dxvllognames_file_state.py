# Generated by Django 5.0.7 on 2024-07-22 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_dxvllognames'),
    ]

    operations = [
        migrations.AddField(
            model_name='dxvllognames',
            name='file_state',
            field=models.BooleanField(default=False),
        ),
    ]