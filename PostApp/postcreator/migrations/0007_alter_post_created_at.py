# Generated by Django 3.2.10 on 2023-04-30 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postcreator', '0006_alter_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime(2023, 5, 1, 1, 12, 27, 663796)),
        ),
    ]
