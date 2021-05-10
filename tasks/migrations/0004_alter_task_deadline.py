# Generated by Django 3.2 on 2021-05-03 12:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Task deadline'),
        ),
    ]