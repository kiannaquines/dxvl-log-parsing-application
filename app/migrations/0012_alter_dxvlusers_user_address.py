# Generated by Django 5.0.7 on 2024-07-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_dxvlusers_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dxvlusers',
            name='user_address',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]