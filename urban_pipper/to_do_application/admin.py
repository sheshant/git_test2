from django.contrib import admin

# Register your models here.

from to_do_application.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'created_at', 'number_of_hours_before_alert', 'due_date', )
    list_filter = ('status', )
    search_fields = ('title', )


admin.site.register(Task, TaskAdmin)

