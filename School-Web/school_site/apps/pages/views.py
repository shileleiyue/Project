from django.shortcuts import render, get_object_or_404
from .models import FlatPage


def page_detail(request, slug):
    page = get_object_or_404(FlatPage, slug=slug, is_published=True)
    context = {'page': page}
    return render(request, 'pages/page_detail.html', context)