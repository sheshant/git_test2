# Generated by Django 2.0 on 2018-08-23 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_application', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='number_of_hours',
            new_name='number_of_hours_before_alert',
        ),
    ]
