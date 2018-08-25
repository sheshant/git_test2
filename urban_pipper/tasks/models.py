from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.db import models

status_choices = (
    ('pending', 'pending'),
    ('completed', 'completed'),
)


class Task(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, default='')
    due_date = models.DateTimeField()
    status = models.CharField(choices=status_choices, max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    hours_before_due_date = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    @property
    def time_interval(self):
        return str(self.due_date - self.created_at)

    @property
    def sub_tasks(self):
        task_list = []
        for task in self.parent_tasks.all():
            task_list.append(task.child_task.title)
        return ', '.join(task_list)

    def delete_task(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    @staticmethod
    def delete_redundant_tasks():
        one_month_old_timestamp = datetime.now() - timedelta(days=30)
        Task.objects.filter(is_deleted=True, deleted_at__lte=one_month_old_timestamp).delete()

    def __str__(self):
        return 'Title = {}, description = {}'.format(self.title, self.description)


class SubTaskMapping(models.Model):
    parent_task = models.ForeignKey(Task, related_name='parent_tasks', on_delete=models.CASCADE)
    child_task = models.ForeignKey(Task, related_name='child_task', on_delete=models.CASCADE)

