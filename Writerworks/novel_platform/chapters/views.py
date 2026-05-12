from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Work,Chapter,OutlineNode
from django.views.decorators.http import require_POST
from django.db.models import Max
from django.db.models.deletion import Collector

# Create your views here.

@require_POST
def outline_delete(request, work_id, node_id):
    node = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    parent = node.parent
    # 提升子节点
    node.children.update(parent=parent)
    # 硬删除该节点（绕过软删除）
    node.delete(using=None)  # 这样会调用模型的 delete，但如果是软删除则不行，需要强制硬删

from datetime import date, timedelta

def work_list(request):
    works = Work.objects.all()
    today = date.today()
    # 今日统计
    today_stats, _ = DailyStats.objects.get_or_create(date=today)
    # 近7天
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    week_stats = DailyStats.objects.filter(date__in=week_dates).order_by('date')
    # 构建日历数据（若某天无记录则补0）
    stats_map = {s.date: s.word_count for s in week_stats}
    calendar_data = []
    for d in week_dates:
        calendar_data.append({
            'date': d.strftime('%m-%d'),
            'words': stats_map.get(d, 0)
        })

    # 工作强度计算
    duration_minutes = today_stats.duration_seconds // 60
    word_count = today_stats.word_count
    # 等级: 低(0-30分钟且<1000字), 中, 高
    if duration_minutes < 30 and word_count < 1000:
        intensity = '低'
        intensity_class = 'low'
    elif duration_minutes < 90 and word_count < 3000:
        intensity = '中'
        intensity_class = 'medium'
    else:
        intensity = '高'
        intensity_class = 'high'
    # 休息提示
    rest_tip = ''
    if duration_minutes > 120 or word_count > 5000:
        rest_tip = '💡 您已工作较长时间，建议休息一下！'

    context = {
        'works': works,
        'today_stats': {
            'words': today_stats.word_count,
            'minutes': duration_minutes,
            'intensity': intensity,
            'intensity_class': intensity_class,
            'rest_tip': rest_tip,
        },
        'calendar_data': calendar_data,
    }
    return render(request, 'chapters/work_list.html', context)

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

from django.utils import timezone
from .models import DailyStats
from datetime import date

def chapter_save(request, work_id, chapter_id):
    if request.method == 'POST':
        chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
        new_content = request.POST.get('content')
        if new_content is not None:
            old_content = chapter.content or ''
            # 计算字数（简单按字符数，可改进）
            new_words = len(new_content)
            old_words = len(old_content)
            word_delta = max(0, new_words - old_words)  # 只增加不计减少

            # 获取上次保存时间（从session或数据库暂存，这里简单用chapter.updated_at）
            # 注意：updated_at 会随每次保存更新，我们需记录上次保存时间，需额外字段或使用session
            # 简便方法：在chapter模型增加 last_saved_at 字段
            # 为简便，我们利用 session 存储每个章节的上次保存时间
            last_save_key = f'chapter_last_save_{chapter_id}'
            last_save_time = request.session.get(last_save_key)
            now = timezone.now()
            duration = 0
            if last_save_time:
                # 转换为datetime
                last_dt = timezone.datetime.fromisoformat(last_save_time)
                duration = (now - last_dt).total_seconds()
                if duration < 0:
                    duration = 0
            # 更新session
            request.session[last_save_key] = now.isoformat()

            # 更新当日统计
            today = date.today()
            stats, created = DailyStats.objects.get_or_create(date=today)
            stats.word_count += word_delta
            stats.duration_seconds += int(duration)
            stats.save()

            # 保存章节内容
            chapter.content = new_content
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

@require_POST
def outline_rename(request, work_id, node_id):
    node = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    node.title = new_title
    node.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': node.title})

@require_POST
def outline_delete(request, work_id, node_id):
    node = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    parent = node.parent
    node.children.update(parent=parent)  # 提升子节点
    OutlineNode._base_manager.filter(id=node_id).delete()  # 硬删除
    return redirect('outline', work_id=work_id)

def about(request):
    return render(request, 'chapters/about.html')
