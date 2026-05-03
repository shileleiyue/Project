from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Work,Chapter
from django.views.decorators.http import require_POST


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

@require_POST
def work_delete(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    work.delete()  # 软删除作品和关联章节
    return redirect('work_list')

def chapter_delete(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    chapter.delete()  # 软删除章节
    return redirect('work_detail', work_id=work_id)
def trash_view(request):
    deleted_works = Work.objects.filter(is_deleted=True).order_by('-created_at')
    deleted_chapters = Chapter.objects.filter(is_deleted=True).order_by('-created_at')
    context = {
        'works': deleted_works,
        'chapters': deleted_chapters,
    }
    return render(request, 'chapters/trash.html', context)

def work_restore(request, work_id):
    work = get_object_or_404(Work, id=work_id, is_deleted=True)
    work.is_deleted = False
    work.save(update_fields=['is_deleted'])
    work.chapters.all().update(is_deleted=False)  # 级联恢复章节
    return redirect('trash')

def chapter_restore(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id, is_deleted=True)
    chapter.is_deleted = False
    chapter.save(update_fields=['is_deleted'])
    return redirect('trash')

def work_hard_delete(request, work_id):
    Work.objects.filter(id=work_id, is_deleted=True).hard_delete()
    return redirect('trash')

@require_POST
def chapter_hard_delete(request, work_id, chapter_id):
    Chapter.objects.filter(id=chapter_id, work_id=work_id, is_deleted=True).hard_delete()
    return redirect('trash')