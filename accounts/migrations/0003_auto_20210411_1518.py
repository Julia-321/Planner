# Generated by Django 3.1.7 on 2021-04-11 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210410_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='home_view',
            field=models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')], default=1),
        ),
    ]
