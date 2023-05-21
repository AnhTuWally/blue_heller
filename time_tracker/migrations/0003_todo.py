# Generated by Django 4.1.7 on 2023-05-13 08:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular object across whole database', primary_key=True, serialize=False, unique=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('priority', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Priority must be between 0 and 100'), django.core.validators.MaxValueValidator(100, message='Priority must be between 0 and 100')])),
                ('is_done', models.BooleanField(default=False)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='time_tracker.task')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
