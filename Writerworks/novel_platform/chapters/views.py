from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Work,Chapter
from django.views.decorators.http import require_POST
from django.db.models import Max

# Create your views here.
def work_list(request):
    works = Work.objects.all()
    return render(request, 'chapters/work_list.html', {'works': works})

def work_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        cover = request.FILES.get('cover_image')
        work = Work.objects.create(title=title, description=description)
        if cover:
            work.cover_image = cover
            work.save()
        return redirect('work_list')
    return render(request, 'chapters/work_create.html')

def work_detail(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    chapters = work.chapters.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            # 查询该作品现有章节的最大 order，若没有则默认为1
            last_order = work.chapters.aggregate(max_order=Max('order'))['max_order'] or 1
            Chapter.objects.create(work=work, title=title, order=last_order + 1)
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
    work.is_deleted = True
    work.save(update_fields=['is_deleted'])
    work.chapters.all().update(is_deleted=True)  # 联级软删除章节
    return redirect('work_list')

def chapter_delete(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    chapter.is_deleted = True
    chapter.save(update_fields=['is_deleted'])
    return redirect('work_detail', work_id=work_id)

def trash_view(request):
    deleted_works = Work._base_manager.filter(is_deleted=True).order_by('-created_at')
    deleted_chapters = Chapter._base_manager.filter(is_deleted=True).order_by('-created_at')
    context = {
        'works': deleted_works,
        'chapters': deleted_chapters,
    }
    return render(request, 'chapters/trash.html', context)

@require_POST
def work_restore(request, work_id):
    work = get_object_or_404(Work._base_manager, id=work_id, is_deleted=True)
    work.is_deleted = False
    work.save(update_fields=['is_deleted'])
    Chapter._base_manager.filter(work_id=work.id).update(is_deleted=False)  # 级联恢复章节
    return redirect('trash')

@require_POST
def chapter_restore(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter._base_manager, id=chapter_id, work_id=work_id, is_deleted=True)
    chapter.is_deleted = False
    chapter.save(update_fields=['is_deleted'])
    return redirect('trash')

@require_POST
def work_hard_delete(request, work_id):
    Work._base_manager.filter(id=work_id, is_deleted=True).delete()
    return redirect('trash')

@require_POST
def chapter_hard_delete(request, work_id, chapter_id):
    Chapter._base_manager.filter(id=chapter_id, work_id=work_id, is_deleted=True).delete()
    return redirect('trash')

def work_rename(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    work.title = new_title
    work.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': work.title})

def chapter_rename(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    chapter.title = new_title
    chapter.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': chapter.title})

def outline_view(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    # 只获取未删除的根节点
    root_nodes = work.outline_nodes.filter(parent__isnull=True).order_by('order')
    return render(request, 'chapters/outline.html', {'work': work, 'root_nodes': root_nodes})

@require_POST
def outline_add_root(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    title = request.POST.get('title', '').strip()
    if title:
        # 获取当前最大 order
        last_order = work.outline_nodes.filter(parent__isnull=True).aggregate(max_order=Max('order'))['max_order'] or 0
        OutlineNode.objects.create(work=work, title=title, parent=None, order=last_order + 1)
    return redirect('outline', work_id=work.id)

@require_POST
def outline_add_child(request, work_id, node_id):
    parent = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    title = request.POST.get('title', '').strip()
    if title:
        last_order = parent.children.aggregate(max_order=Max('order'))['max_order'] or 0
        OutlineNode.objects.create(work=parent.work, title=title, parent=parent, order=last_order + 1)
    return redirect('outline', work_id=work_id)

