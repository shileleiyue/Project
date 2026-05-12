from django.shortcuts import render
from .models import Department, Leader, Teacher


def departments(request):
    departments = Department.objects.prefetch_related('teachers').all()
    context = {'departments': departments}
    return render(request, 'organization/departments.html', context)


def department_detail(request, slug):
    department = Department.objects.prefetch_related('teachers').get(slug=slug)
    context = {'department': department}
    return render(request, 'organization/department_detail.html', context)


def leaders(request):
    leaders = Leader.objects.all()
    context = {'leaders': leaders}
    return render(request, 'organization/leaders.html', context)


def teachers(request):
    teachers = Teacher.objects.select_related('department').all()
    context = {'teachers': teachers}
    return render(request, 'organization/teachers.html', context)