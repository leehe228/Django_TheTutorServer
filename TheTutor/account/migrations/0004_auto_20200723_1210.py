# Generated by Django 2.0.13 on 2020-07-23 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200723_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_day',
            field=models.CharField(default='0&0&0&0&0&0&0', max_length=30),
        ),
    ]