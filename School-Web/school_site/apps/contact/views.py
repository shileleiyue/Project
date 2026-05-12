from django.shortcuts import render, redirect
from .forms import MessageForm, PrincipalMailForm
from .models import Message


def message_list(request):
    messages_list = Message.objects.filter(is_public=True)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:message_list')
    else:
        form = MessageForm()
    return render(request, 'contact/message_list.html', {'messages_list': messages_list, 'form': form})


def principal_mail(request):
    if request.method == 'POST':
        form = PrincipalMailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:mail_success')
    else:
        form = PrincipalMailForm()
    return render(request, 'contact/principal_mail.html', {'form': form})


def mail_success(request):
    return render(request, 'contact/mail_success.html')