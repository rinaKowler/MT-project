# Generated by Django 4.0 on 2021-12-22 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_volunteer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='volunteer_place_name',
            field=models.CharField(default=7, max_length=200),
            preserve_default=False,
        ),
    ]
