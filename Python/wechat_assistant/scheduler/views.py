import re
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Schedule, Todo


@login_required
def schedule_list(request):
    schedules = Schedule.objects.all()
    view = request.GET.get('view', 'list')
    date = request.GET.get('date', '')
    if date:
        schedules = schedules.filter(start_time__date=date)
    return render(request, 'schedules.html', {
        'schedules': schedules,
        'view': view,
        'date': date,
    })


@login_required
def schedule_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        if title and start_time:
            Schedule.objects.create(
                title=title,
                start_time=start_time,
                end_time=end_time or None,
                location=location,
                description=description,
            )
        return redirect('schedule_list')
    return render(request, 'schedule_form.html')


@login_required
def schedule_edit(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.title = request.POST.get('title', schedule.title)
        schedule.start_time = request.POST.get('start_time', schedule.start_time)
        schedule.end_time = request.POST.get('end_time') or None
        schedule.location = request.POST.get('location', '')
        schedule.description = request.POST.get('description', '')
        schedule.status = request.POST.get('status', schedule.status)
        schedule.save()
        return redirect('schedule_list')
    return render(request, 'schedule_form.html', {'schedule': schedule})


@login_required
def schedule_delete(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule_list')
    return render(request, 'schedule_confirm_delete.html', {'schedule': schedule})


@login_required
def todo_list(request):
    todos = Todo.objects.all()
    query = request.GET.get('q', '')
    priority = request.GET.get('priority', '')
    if query:
        todos = todos.filter(Q(title__icontains=query))
    if priority:
        todos = todos.filter(priority=priority)
    return render(request, 'todos.html', {'todos': todos})


@login_required
def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date', '')
        if title:
            Todo.objects.create(
                title=title,
                priority=priority,
                due_date=due_date or None,
            )
        return redirect('todo_list')
    return render(request, 'todo_form.html')


@login_required
def todo_toggle(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_done = not todo.is_done
    todo.save()
    return JsonResponse({'is_done': todo.is_done})


@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo_confirm_delete.html', {'todo': todo})


@login_required
def extract_schedule_from_message(request, message_id):
    from core.models import Message
    message = get_object_or_404(Message, id=message_id)
    content = message.content
    patterns = [
        (r'(?:明天|今天|后天)\s*(?:[早中晚上下午]*)\s*(\d{1,2}[:：]\d{2})\s*(.+?)(?:。|$)', 1),
        (r'(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)\s*(\d{1,2}[:：]\d{2})?\s*(.+?)(?:。|$)', 2),
    ]
    title = content[:50] if len(content) > 50 else content
    start_time = datetime.now() + timedelta(hours=1)
    for pattern, _ in patterns:
        match = re.search(pattern, content)
        if match:
            title = match.group(min(len(match.groups()), 3))
            break
    Schedule.objects.create(
        title=title,
        description=content,
        start_time=start_time,
        source_msg=message,
        status='pending',
    )
    return redirect('schedule_list')