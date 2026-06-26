from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.db.models import Q
from .models import Contact, Message, Tag, Conversation
from scheduler.models import Schedule, Todo


class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def dashboard(request):
    total_contacts = Contact.objects.count()
    total_messages = Message.objects.count()
    total_starred = Message.objects.filter(is_starred=True).count()
    total_schedules = Schedule.objects.filter(status__in=['pending', 'confirmed']).count()
    pending_todos = Todo.objects.filter(is_done=False).count()
    recent_conversations = Conversation.objects.filter(is_archived=False)[:10]
    upcoming_schedules = Schedule.objects.filter(status__in=['pending', 'confirmed'])[:5]
    return render(request, 'dashboard.html', {
        'total_contacts': total_contacts,
        'total_messages': total_messages,
        'total_starred': total_starred,
        'total_schedules': total_schedules,
        'pending_todos': pending_todos,
        'recent_conversations': recent_conversations,
        'upcoming_schedules': upcoming_schedules,
    })


@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    query = request.GET.get('q', '')
    if query:
        contacts = contacts.filter(Q(name__icontains=query) | Q(remark__icontains=query))
    return render(request, 'contacts.html', {'contacts': contacts, 'query': query})


@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    messages = Message.objects.filter(contact=contact)[:100]
    return render(request, 'contact_detail.html', {'contact': contact, 'messages': messages})


@login_required
def message_list(request):
    messages = Message.objects.all().select_related('contact')
    query = request.GET.get('q', '')
    msg_type = request.GET.get('type', '')
    tag_id = request.GET.get('tag', '')
    starred = request.GET.get('starred', '')
    if query:
        messages = messages.filter(Q(content__icontains=query))
    if msg_type:
        messages = messages.filter(msg_type=msg_type)
    if tag_id:
        messages = messages.filter(tags__id=tag_id)
    if starred:
        messages = messages.filter(is_starred=True)
    tags = Tag.objects.all()
    return render(request, 'messages.html', {
        'messages': messages,
        'tags': tags,
        'query': query,
        'msg_type': msg_type,
        'tag_id': tag_id,
        'starred': starred,
    })


@login_required
def toggle_star(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_starred = not message.is_starred
    message.save()
    return JsonResponse({'is_starred': message.is_starred})


@login_required
def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#1890ff')
        if name:
            Tag.objects.get_or_create(name=name, defaults={'color': color})
    return redirect('message_list')


@login_required
def tag_message(request, message_id, tag_id):
    message = get_object_or_404(Message, id=message_id)
    tag = get_object_or_404(Tag, id=tag_id)
    if tag in message.tags.all():
        message.tags.remove(tag)
    else:
        message.tags.add(tag)
    return redirect('message_list')


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(is_archived=False).select_related('contact', 'last_message')
    archived = request.GET.get('archived', '')
    if archived:
        conversations = Conversation.objects.filter(is_archived=True).select_related('contact', 'last_message')
    return render(request, 'conversations.html', {'conversations': conversations, 'archived': archived})


@login_required
def toggle_archive(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.is_archived = not conversation.is_archived
    conversation.save()
    return redirect('conversation_list')