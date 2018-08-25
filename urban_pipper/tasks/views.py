from datetime import datetime, timedelta

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Task
from .forms import TaskForm
import pytz


def get_task_list(request):
    submitted_data = request.GET
    due_date_filter = submitted_data.get('due_date_filter', '')
    task_list = Task.objects.filter(is_deleted=False, title__icontains=submitted_data.get('title', '')).order_by('-due_date')
    start_date = datetime.now()

    if due_date_filter == 'today':
        end_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        task_list = task_list.filter(due_date__gte=start_date, due_date__lte=end_date)

    elif due_date_filter == 'this_week':
        end_date = start_date + timedelta(6 - start_date.weekday())
        task_list = task_list.filter(due_date__gte=start_date, due_date__lte=end_date)

    elif due_date_filter == 'next_week':
        end_date = start_date + timedelta(13 - start_date.weekday())
        task_list = task_list.filter(due_date__gte=start_date, due_date__lte=end_date)

    elif due_date_filter == 'overdue':
        end_date = datetime.now()
        task_list = task_list.filter(due_date__lte=end_date)

    return task_list


def get_messages(request):
    for task in Task.objects.filter(is_deleted=False, due_date__gte=datetime.now(), status='pending'):
        if datetime.now().replace(tzinfo=pytz.UTC) >= task.due_date.replace(tzinfo=pytz.UTC) - \
                timedelta(hours=task.hours_before_due_date):
            messages.warning(request, 'Task {} to get due in {}.'.format(task.title, task.due_date))


def task_list(request):
    tasks = get_task_list(request)
    get_messages(request)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def save_task_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            tasks = Task.objects.filter(is_deleted=False)
            data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html', {
                'tasks': tasks
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
    else:
        form = TaskForm()
    return save_task_form(request, form, 'tasks/includes/partial_task_create.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
    else:
        form = TaskForm(instance=task)
    return save_task_form(request, form, 'tasks/includes/partial_task_update.html')


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = dict()
    if request.method == 'POST':
        task.delete_task()
        data['form_is_valid'] = True
        tasks = Task.objects.filter(is_deleted=False)
        data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html', {
            'tasks': tasks
        })
    else:
        context = {'task': task}
        data['html_form'] = render_to_string('tasks/includes/partial_task_delete.html', context, request=request)
    return JsonResponse(data)
