# Generated by Django 4.2.1 on 2023-10-14 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_remove_todorepeat_todo_todo_todo_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='todorepeat',
            name='repeat_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
