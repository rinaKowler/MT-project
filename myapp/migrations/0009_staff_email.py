# Generated by Django 4.0 on 2021-12-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_event_event_date_alter_nightout_trip_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]