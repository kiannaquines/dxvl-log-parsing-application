# Generated by Django 5.0.7 on 2024-07-30 08:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisements',
            fields=[
                ('advertisement_id', models.UUIDField(default=uuid.UUID('b7284806-78e1-4775-8a85-92f412b8e1f9'), editable=False, primary_key=True, serialize=False)),
                ('advertisement_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.dxvllogs')),
            ],
        ),
    ]