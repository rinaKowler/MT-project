# Generated by Django 4.0 on 2022-02-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_atteendence'),
    ]

    operations = [
        migrations.AddField(
            model_name='atteendence',
            name='attendence',
            field=models.BooleanField(default=False),
        ),
    ]
