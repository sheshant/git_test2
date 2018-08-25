from django.contrib import admin

# Register your models here.
from tasks.models import Task, SubTaskMapping


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'status', 'created_at', 'time_interval', 'is_deleted')
    search_fields = ['title' ]
    list_filter = ('status', 'is_deleted')


admin.site.register(Task, TaskAdmin)


class SubTaskMappingAdmin(admin.ModelAdmin):
    list_display = ('parent_task', 'child_task')


admin.site.register(SubTaskMapping, SubTaskMappingAdmin)

