from django.http import JsonResponse
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

def chapter_read(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    work = chapter.work
    context = {
        'chapter': chapter,
        'work': work,
    }
    return render(request, 'chapters/chapter_read.html', context)

def chapter_save(request, work_id, chapter_id):
    if request.method == 'POST':
        chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
        content = request.POST.get('content')
        if content is not None:
            chapter.content = content
            chapter.save()
            return JsonResponse({'success': True, 'updated_at': chapter.updated_at.isoformat()})
    return JsonResponse({'error': 'Invalid method'}, status=405)