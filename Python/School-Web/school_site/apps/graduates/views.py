from django.shortcuts import render
from .models import Graduate


def graduate_list(request):
    graduates = Graduate.objects.all()
    return render(request, 'graduates/list.html', {'graduates': graduates})