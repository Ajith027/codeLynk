# Generated by Django 3.2.10 on 2023-04-30 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='ViwedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('unlike', models.BooleanField(default=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postcreator.post')),
            ],
        ),
    ]
