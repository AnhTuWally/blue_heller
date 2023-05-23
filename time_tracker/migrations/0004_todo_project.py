# Generated by Django 4.1.7 on 2023-05-17 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0003_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='time_tracker.project'),
        ),
    ]