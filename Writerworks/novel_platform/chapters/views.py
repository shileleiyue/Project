from django.shortcuts import render, redirect,get_object_or_404
from .models import Work,Chapter

# Create your views here.
def work_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:  # 至少标题不为空
            Work.objects.create(title=title, description=description)
        return redirect('work_list')
    works = Work.objects.all()
    return render(request, 'chapters/work_list.html', {'works': works})
def work_detail(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    chapters = work.chapters.order_by('-created_at')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Chapter.objects.create(work=work, title=title)
        return redirect('work_detail', work_id=work.id)
    
    context = {
        'work': work,
        'chapters': chapters,
    }
    return render(request, 'chapters/work_detail.html', context)