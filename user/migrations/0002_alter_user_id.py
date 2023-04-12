# Generated by Django 4.1.7 on 2023-04-10 10:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular object across whole database', primary_key=True, serialize=False, unique=True),
        ),
    ]
