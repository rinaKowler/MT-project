# Generated by Django 4.0 on 2022-02-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_alter_payment_purchased_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='purchased_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
