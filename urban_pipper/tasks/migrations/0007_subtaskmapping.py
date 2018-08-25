# Generated by Django 2.0 on 2018-08-25 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTaskMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_task', to='tasks.Task')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_tasks', to='tasks.Task')),
            ],
        ),
    ]
