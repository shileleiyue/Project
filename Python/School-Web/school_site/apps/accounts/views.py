from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import uuid
from .forms import LoginForm, ParentBindForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        auth_login(request, user)

        # 班级账户生成长期令牌
        if user.role == 'whiteboard':
            token = uuid.uuid4().hex
            user.whiteboard_token = token
            user.token_expiry = timezone.now() + timedelta(days=365)
            user.save()

        next_url = request.GET.get('next', 'core:home')
        return redirect(next_url)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('core:home')


@login_required
def parent_bind(request):
    if request.user.role != 'parent':
        return redirect('core:home')

    form = ParentBindForm(request.POST or None, parent_user=request.user)
    if request.method == 'POST' and form.is_valid():
        student = form.save()
        messages.success(request, f'成功绑定学生：{student.real_name}')
        return redirect('core:home')

    return render(request, 'accounts/bind.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')