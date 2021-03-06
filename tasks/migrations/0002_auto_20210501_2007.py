# Generated by Django 3.2 on 2021-05-01 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Creation date time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Task deadline'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=2000, verbose_name='Description'),
        ),
    ]
