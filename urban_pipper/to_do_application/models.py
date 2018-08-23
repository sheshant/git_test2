from django.db import models

# Create your models here.

status_choices = (
    ('PENDING', 'pending'),
    ('COMPLETED', 'completed'),
)


class Task(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=1000, unique=True)
    status = models.CharField(choices=status_choices, default='pending', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_hours_before_alert = models.IntegerField()
    due_date = models.DateTimeField()



