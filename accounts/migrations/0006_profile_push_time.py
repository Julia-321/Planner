# Generated by Django 3.2 on 2021-05-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210424_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='push_time',
            field=models.IntegerField(choices=[(1, 'deadline'), (2, '15 min'), (3, 'hour'), (4, '1 min')], default=1),
        ),
    ]
