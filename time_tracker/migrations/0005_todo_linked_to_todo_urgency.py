# Generated by Django 4.1.7 on 2023-05-21 21:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0004_todo_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='linked_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='time_tracker.todo'),
        ),
        migrations.AddField(
            model_name='todo',
            name='urgency',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Urgency must be between 0 and 5'), django.core.validators.MaxValueValidator(5, message='Urgency must be between 0 and 5')]),
        ),
    ]
