# Generated by Django 3.2.10 on 2023-04-30 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postviewer', '0002_rename_viwedpost_viewedpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedpost',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
