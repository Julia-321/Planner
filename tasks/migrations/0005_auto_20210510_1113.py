# Generated by Django 3.1.7 on 2021-05-10 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_deadline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['complete', 'created']},
        ),
    ]
