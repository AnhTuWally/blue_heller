# Generated by Django 4.2.1 on 2023-11-07 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0006_delete_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='activetask',
            name='note',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
