# Generated by Django 4.0 on 2022-01-30 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_remove_studentlecture_describe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentlecture',
            name='lecture1',
        ),
        migrations.RemoveField(
            model_name='studentlecture',
            name='lecture2',
        ),
        migrations.AddField(
            model_name='studentlecture',
            name='monday_lecture1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='monday_lecture1', to='myapp.lecture'),
        ),
        migrations.AddField(
            model_name='studentlecture',
            name='monday_lecture2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='monday_lecture2', to='myapp.lecture'),
        ),
        migrations.AddField(
            model_name='studentlecture',
            name='sunady_lecture2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='sunday_lecture2', to='myapp.lecture'),
        ),
        migrations.AddField(
            model_name='studentlecture',
            name='sunday_lecture1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='sunday_lecture1', to='myapp.lecture'),
        ),
    ]
