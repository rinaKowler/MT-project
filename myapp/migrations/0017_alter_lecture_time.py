# Generated by Django 4.0 on 2022-01-29 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_lecture_alter_payment_amount_studentlecture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
