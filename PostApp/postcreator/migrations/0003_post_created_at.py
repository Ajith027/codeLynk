# Generated by Django 3.2.10 on 2023-04-30 17:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postcreator', '0002_auto_20230430_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime(2023, 4, 30, 23, 9, 36, 697036)),
        ),
    ]