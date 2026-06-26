from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Work, Chapter, OutlineNode, DailyStats, WritingGoal, Character, Relationship, TimelineEvent, TechNode, Category, Tag
from django.views.decorators.http import require_POST
from django.db.models import Max, Sum, Q
from django.db.models.deletion import Collector
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
import json

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            messages.error(request, '两次密码输入不一致')
            return render(request, 'core/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'core/register.html')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('work_list')
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('work_list')
        else:
            messages.error(request, '用户名或密码错误')
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def work_list(request):
    works_list = Work.objects.filter(user=request.user).order_by('-created_at')

    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    if category_id:
        works_list = works_list.filter(category_id=category_id)
    if tag_id:
        works_list = works_list.filter(tags__id=tag_id)

    from django.conf import settings as dj_settings
    page_size = dj_settings.APP_CONFIG.get('page_size', 10)
    paginator = Paginator(works_list, page_size)
    page_number = request.GET.get('page')
    works = paginator.get_page(page_number)
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

    categories = Category.objects.all()
    tags = Tag.objects.all()

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
        'categories': categories,
        'tags': tags,
        'selected_category': category_id,
        'selected_tag': tag_id,
    }
    return render(request, 'core/work_list.html', context)

@login_required(login_url='login')
def work_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        cover = request.FILES.get('cover_image')
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        work = Work.objects.create(
            title=title,
            description=description,
            user=request.user,
            category_id=category_id if category_id else None
        )
        if tag_ids:
            work.tags.set(tag_ids)
        if cover:
            work.cover_image = cover
            work.save()
        return redirect('work_list')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/work_create.html', {
        'categories': categories,
        'tags': tags,
        'works': works,
    })

@login_required(login_url='login')
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
        
    works = Work.objects.filter(user=request.user, is_deleted=False)
    context = {
        'work': work,
        'chapters': chapters,
        'works': works,
    }
    return render(request, 'core/work_detail.html', context)

@login_required(login_url='login')
def chapter_read(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    work = chapter.work
    works = Work.objects.filter(user=request.user, is_deleted=False)
    context = {
        'chapter': chapter,
        'work': work,
        'works': works,
    }
    return render(request, 'core/chapter_read.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
@require_POST
def work_delete(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    work.is_deleted = True
    work.save(update_fields=['is_deleted'])
    work.chapters.all().update(is_deleted=True)  # 联级软删除章节
    return redirect('work_list')

@login_required(login_url='login')
def chapter_delete(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    chapter.is_deleted = True
    chapter.save(update_fields=['is_deleted'])
    return redirect('work_detail', work_id=work_id)

@login_required(login_url='login')
def trash_view(request):
    deleted_works = Work._base_manager.filter(is_deleted=True).order_by('-created_at')
    deleted_chapters = Chapter._base_manager.filter(is_deleted=True).order_by('-created_at')
    works = Work.objects.filter(user=request.user, is_deleted=False)
    context = {
        'deleted_works': deleted_works,
        'chapters': deleted_chapters,
        'works': works,
    }
    return render(request, 'core/trash.html', context)

@login_required(login_url='login')
@require_POST
def work_restore(request, work_id):
    work = get_object_or_404(Work._base_manager, id=work_id, is_deleted=True)
    work.is_deleted = False
    work.save(update_fields=['is_deleted'])
    Chapter._base_manager.filter(work_id=work.id).update(is_deleted=False)  # 级联恢复章节
    return redirect('trash')

@login_required(login_url='login')
@require_POST
def chapter_restore(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter._base_manager, id=chapter_id, work_id=work_id, is_deleted=True)
    chapter.is_deleted = False
    chapter.save(update_fields=['is_deleted'])
    return redirect('trash')

@login_required(login_url='login')
@require_POST
def work_hard_delete(request, work_id):
    Work._base_manager.filter(id=work_id, is_deleted=True).delete()
    return redirect('trash')

@login_required(login_url='login')
@require_POST
def chapter_hard_delete(request, work_id, chapter_id):
    Chapter._base_manager.filter(id=chapter_id, work_id=work_id, is_deleted=True).delete()
    return redirect('trash')

@login_required(login_url='login')
def work_rename(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    work.title = new_title
    work.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': work.title})

@login_required(login_url='login')
def chapter_rename(request, work_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, work_id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    chapter.title = new_title
    chapter.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': chapter.title})

@login_required(login_url='login')
def outline_view(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    # 只获取未删除的根节点
    root_nodes = work.outline_nodes.filter(parent__isnull=True).order_by('order')
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/outline.html', {'work': work, 'root_nodes': root_nodes, 'works': works})

@login_required(login_url='login')
@require_POST
def outline_add_root(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    title = request.POST.get('title', '').strip()
    if title:
        # 获取当前最大 order
        last_order = work.outline_nodes.filter(parent__isnull=True).aggregate(max_order=Max('order'))['max_order'] or 0
        OutlineNode.objects.create(work=work, title=title, parent=None, order=last_order + 1)
    return redirect('outline', work_id=work.id)

@login_required(login_url='login')
@require_POST
def outline_add_child(request, work_id, node_id):
    parent = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    title = request.POST.get('title', '').strip()
    if title:
        last_order = parent.children.aggregate(max_order=Max('order'))['max_order'] or 0
        OutlineNode.objects.create(work=parent.work, title=title, parent=parent, order=last_order + 1)
    return redirect('outline', work_id=work_id)

@login_required(login_url='login')
@require_POST
def outline_rename(request, work_id, node_id):
    node = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    new_title = request.POST.get('title', '').strip()
    if not new_title:
        return JsonResponse({'success': False, 'error': '标题不能为空'}, status=400)
    node.title = new_title
    node.save(update_fields=['title'])
    return JsonResponse({'success': True, 'title': node.title})

@login_required(login_url='login')
@require_POST
def outline_delete(request, work_id, node_id):
    node = get_object_or_404(OutlineNode, id=node_id, work_id=work_id)
    parent = node.parent
    node.children.update(parent=parent)  # 提升子节点
    OutlineNode._base_manager.filter(id=node_id).delete()  # 硬删除
    return redirect('outline', work_id=work_id)

@login_required(login_url='login')
def about(request):
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/about.html', {'works': works})

@login_required(login_url='login')
def stats_view(request):
    today = date.today()
    today_stats, _ = DailyStats.objects.get_or_create(date=today)

    month_start = today - timedelta(days=30)
    month_stats = DailyStats.objects.filter(date__gte=month_start, date__lte=today).order_by('date')

    total_words = DailyStats.objects.aggregate(total=Sum('word_count'))['total'] or 0
    total_duration = DailyStats.objects.aggregate(total=Sum('duration_seconds'))['total'] or 0

    week_start = today - timedelta(days=today.weekday())
    week_stats = DailyStats.objects.filter(date__gte=week_start).aggregate(
        words=Sum('word_count'), duration=Sum('duration_seconds')
    )

    goal, _ = WritingGoal.objects.get_or_create(user=request.user)

    chart_labels = []
    chart_data = []
    chart_items = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        chart_labels.append(d.strftime('%m-%d'))
        day_stat = month_stats.filter(date=d).first()
        val = day_stat.word_count if day_stat else 0
        chart_data.append(val)
        chart_items.append({'label': d.strftime('%m-%d'), 'value': val})

    weekly_words = week_stats['words'] or 0
    weekly_progress = min(100, int(weekly_words / goal.weekly_goal * 100)) if goal.weekly_goal > 0 else 0
    daily_progress = min(100, int(today_stats.word_count / goal.daily_goal * 100)) if goal.daily_goal > 0 else 0

    context = {
        'today_words': today_stats.word_count,
        'today_minutes': today_stats.duration_seconds // 60,
        'total_words': total_words,
        'total_hours': total_duration // 3600,
        'weekly_words': weekly_words,
        'month_avg_words': total_words // 30 if total_words > 0 else 0,
        'daily_goal': goal.daily_goal,
        'weekly_goal': goal.weekly_goal,
        'daily_progress': daily_progress,
        'weekly_progress': weekly_progress,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'chart_items': chart_items,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
        'works': Work.objects.filter(user=request.user, is_deleted=False),
    }
    return render(request, 'core/stats.html', context)

@login_required(login_url='login')
def stats_update_goal(request):
    if request.method == 'POST':
        goal, _ = WritingGoal.objects.get_or_create(user=request.user)
        goal.daily_goal = int(request.POST.get('daily_goal', 1000))
        goal.weekly_goal = int(request.POST.get('weekly_goal', 7000))
        goal.save()
        return redirect('stats')
    return redirect('work_list')


# ---------- 角色管理 ----------
@login_required(login_url='login')
def character_list(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    characters = work.characters.all()
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/character_list.html', {'work': work, 'characters': characters, 'works': works})


@login_required(login_url='login')
def character_add(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias', '')
        gender = request.POST.get('gender', '')
        age = request.POST.get('age')
        description = request.POST.get('description', '')
        Character.objects.create(
            work=work, name=name, alias=alias,
            gender=gender, age=age if age else None,
            description=description
        )
        return redirect('character_list', work_id=work.id)
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/character_form.html', {'work': work, 'character': None, 'works': works})


@login_required(login_url='login')
def character_edit(request, work_id, char_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    char = get_object_or_404(Character, id=char_id, work=work)
    if request.method == 'POST':
        char.name = request.POST.get('name')
        char.alias = request.POST.get('alias', '')
        char.gender = request.POST.get('gender', '')
        age = request.POST.get('age')
        char.age = int(age) if age else None
        char.description = request.POST.get('description', '')
        char.save()
        return redirect('character_list', work_id=work.id)
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/character_form.html', {'work': work, 'character': char, 'works': works})


@login_required(login_url='login')
@require_POST
def character_delete(request, work_id, char_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    char = get_object_or_404(Character, id=char_id, work=work)
    Relationship.objects.filter(
        Q(character1=char) | Q(character2=char)
    ).delete()
    char.timeline_events.clear()
    char.delete()
    return redirect('character_list', work_id=work.id)


# ---------- 关系管理 ----------
@login_required(login_url='login')
def relationship_list(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    relationships = Relationship.objects.filter(
        Q(character1__work=work) | Q(character2__work=work)
    ).distinct()
    works = Work.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'core/relationship_list.html', {'work': work, 'relationships': relationships, 'works': works})


@login_required(login_url='login')
def relationship_add(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    characters = work.characters.all()
    if request.method == 'POST':
        char1_id = request.POST.get('character1')
        char2_id = request.POST.get('character2')
        relation_type = request.POST.get('relation_type')
        description = request.POST.get('description', '')
        if char1_id and char2_id and char1_id != char2_id:
            char1 = get_object_or_404(Character, id=char1_id, work=work)
            char2 = get_object_or_404(Character, id=char2_id, work=work)
            if int(char1_id) > int(char2_id):
                char1, char2 = char2, char1
            existing = Relationship.objects.filter(character1=char1, character2=char2).first()
            if not existing:
                Relationship.objects.create(
                    character1=char1, character2=char2,
                    relation_type=relation_type, description=description
                )
        return redirect('relationship_list', work_id=work.id)
    return render(request, 'core/relationship_form.html', {
        'work': work, 'relationship': None, 'characters': characters
    })


@login_required(login_url='login')
def relationship_edit(request, work_id, rel_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    rel = get_object_or_404(Relationship, id=rel_id)
    characters = work.characters.all()
    if request.method == 'POST':
        char1_id = request.POST.get('character1')
        char2_id = request.POST.get('character2')
        relation_type = request.POST.get('relation_type')
        description = request.POST.get('description', '')
        if char1_id and char2_id and char1_id != char2_id:
            char1 = get_object_or_404(Character, id=char1_id, work=work)
            char2 = get_object_or_404(Character, id=char2_id, work=work)
            if int(char1_id) > int(char2_id):
                char1, char2 = char2, char1
            rel.character1 = char1
            rel.character2 = char2
            rel.relation_type = relation_type
            rel.description = description
            rel.save()
        return redirect('relationship_list', work_id=work.id)
    return render(request, 'core/relationship_form.html', {
        'work': work, 'relationship': rel, 'characters': characters
    })


@login_required(login_url='login')
@require_POST
def relationship_delete(request, work_id, rel_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    rel = get_object_or_404(Relationship, id=rel_id)
    rel.delete()
    return redirect('relationship_list', work_id=work.id)


# ---------- 时间线管理 ----------
@login_required(login_url='login')
def timeline_list(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    events = work.timeline_events.all().order_by('date')
    return render(request, 'core/timeline_list.html', {'work': work, 'events': events})


@login_required(login_url='login')
def timeline_add(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    characters = work.characters.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        date_val = request.POST.get('date', '')
        description = request.POST.get('description', '')
        event = TimelineEvent.objects.create(
            work=work, title=title, date=date_val, description=description
        )
        char_ids = request.POST.getlist('characters')
        if char_ids:
            event.characters.add(*char_ids)
        return redirect('timeline_list', work_id=work.id)
    return render(request, 'core/timeline_form.html', {
        'work': work, 'event': None, 'characters': characters, 'selected': []
    })


@login_required(login_url='login')
def timeline_edit(request, work_id, event_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    event = get_object_or_404(TimelineEvent, id=event_id, work=work)
    characters = work.characters.all()
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.date = request.POST.get('date', '')
        event.description = request.POST.get('description', '')
        event.save()
        event.characters.clear()
        char_ids = request.POST.getlist('characters')
        if char_ids:
            event.characters.add(*char_ids)
        return redirect('timeline_list', work_id=work.id)
    selected_ids = list(event.characters.values_list('id', flat=True))
    return render(request, 'core/timeline_form.html', {
        'work': work, 'event': event, 'characters': characters, 'selected': selected_ids
    })


@login_required(login_url='login')
@require_POST
def timeline_delete(request, work_id, event_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    event = get_object_or_404(TimelineEvent, id=event_id, work=work)
    event.delete()
    return redirect('timeline_list', work_id=work.id)


# ---------- 科技树管理 ----------
@login_required(login_url='login')
def tech_tree(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    nodes = work.tech_nodes.all()

    def build_tree(nodes_list, parent_id=None):
        tree = []
        for node in nodes_list:
            if node.parent_id == parent_id:
                children = build_tree(nodes_list, node.id)
                node.children_list = children
                tree.append(node)
        return tree

    tree = build_tree(list(nodes))
    return render(request, 'core/tech_tree.html', {'work': work, 'tree': tree})


@login_required(login_url='login')
def tech_add(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    parents = work.tech_nodes.all()
    preselected_parent_id = request.GET.get('parent_id')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        parent_id = request.POST.get('parent_id')
        parent = get_object_or_404(TechNode, id=parent_id, work=work) if parent_id else None
        TechNode.objects.create(work=work, name=name, description=description, parent=parent)
        return redirect('tech_tree', work_id=work.id)
    return render(request, 'core/tech_form.html', {
        'work': work, 'node': None, 'parents': parents, 'preselected_parent_id': preselected_parent_id
    })


@login_required(login_url='login')
def tech_edit(request, work_id, node_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    node = get_object_or_404(TechNode, id=node_id, work=work)
    parents = work.tech_nodes.exclude(id=node.id)
    if request.method == 'POST':
        node.name = request.POST.get('name')
        node.description = request.POST.get('description', '')
        parent_id = request.POST.get('parent_id')
        node.parent = get_object_or_404(TechNode, id=parent_id, work=work) if parent_id else None
        node.save()
        return redirect('tech_tree', work_id=work.id)
    return render(request, 'core/tech_form.html', {
        'work': work, 'node': node, 'parents': parents
    })


@login_required(login_url='login')
@require_POST
def tech_delete(request, work_id, node_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    node = get_object_or_404(TechNode, id=node_id, work=work)
    node.children.update(parent=None)
    node.delete()
    return redirect('tech_tree', work_id=work.id)

@login_required(login_url='login')
def export_work_txt(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    chapters = work.chapters.all().order_by('order', 'created_at')
    lines = [f"《{work.title}》\n", f"简介：{work.description}\n", "=" * 40 + "\n"]
    for ch in chapters:
        lines.append(f"\n## {ch.title}\n\n")
        lines.append(ch.content or "")
        lines.append("\n")
    content = "".join(lines)
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{work.title}.txt"'
    return response

@login_required(login_url='login')
def search_view(request):
    query = request.GET.get('q', '').strip()
    works = []
    chapters = []
    characters = []

    if query:
        works = Work.objects.filter(
            Q(user=request.user),
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        chapters = Chapter.objects.filter(
            Q(work__user=request.user),
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        characters = Character.objects.filter(
            Q(work__user=request.user),
            Q(name__icontains=query) | Q(alias__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'query': query,
        'search_works': works,
        'chapters': chapters,
        'characters': characters,
        'works': Work.objects.filter(user=request.user, is_deleted=False),
    }
    return render(request, 'core/search_results.html', context)

@login_required(login_url='login')
def export_work_json(request, work_id):
    work = get_object_or_404(Work, id=work_id, user=request.user)
    chapters = work.chapters.all().order_by('order', 'created_at')
    data = {
        'title': work.title,
        'description': work.description,
        'chapters': [{'title': ch.title, 'content': ch.content} for ch in chapters],
    }
    response = JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="{work.title}.json"'
    return response


# ---------- 应用设置 ----------
@login_required(login_url='login')
def app_settings_view(request):
    """设置页：存储位置、个性化、写作偏好、账号信息。"""
    from django.conf import settings as dj_settings
    from . import app_config

    data_dir = dj_settings.DATA_DIR
    cfg = dj_settings.APP_CONFIG
    works = Work.objects.filter(user=request.user, is_deleted=False)
    goal, _ = WritingGoal.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        section = request.POST.get('section', '')

        if section == 'personalization':
            updates = {
                'theme_primary': request.POST.get('theme_primary', cfg['theme_primary']),
                'theme_accent': request.POST.get('theme_accent', cfg['theme_accent']),
                'font_scale': float(request.POST.get('font_scale', 1.0)),
                'display_name': request.POST.get('display_name', '').strip(),
            }
            cfg = app_config.save_config(data_dir, updates)
            dj_settings.APP_CONFIG = cfg
            messages.success(request, '个性化设置已保存，刷新后生效。')
            return redirect('app_settings')

        elif section == 'preferences':
            updates = {
                'page_size': max(5, min(50, int(request.POST.get('page_size', 10)))),
                'autosave': request.POST.get('autosave') == 'on',
            }
            cfg = app_config.save_config(data_dir, updates)
            dj_settings.APP_CONFIG = cfg
            messages.success(request, '写作偏好已保存。')
            return redirect('app_settings')

        elif section == 'goal':
            goal.daily_goal = int(request.POST.get('daily_goal', 1000))
            goal.weekly_goal = int(request.POST.get('weekly_goal', 7000))
            goal.save()
            messages.success(request, '写作目标已更新。')
            return redirect('app_settings')

    context = {
        'works': works,
        'cfg': cfg,
        'data_dir': str(data_dir),
        'goal': goal,
        'default_data_dir': str(app_config.BOOTSTRAP_DIR),
    }
    return render(request, 'core/settings.html', context)


@login_required(login_url='login')
@require_POST
def app_settings_password(request):
    """修改当前登录用户密码。"""
    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    confirm = request.POST.get('confirm_password', '')

    user = request.user
    if not user.check_password(old_password):
        messages.error(request, '原密码不正确。')
        return redirect('app_settings')
    if len(new_password) < 6:
        messages.error(request, '新密码长度至少 6 位。')
        return redirect('app_settings')
    if new_password != confirm:
        messages.error(request, '两次输入的新密码不一致。')
        return redirect('app_settings')

    user.set_password(new_password)
    user.save()
    # 修改密码后会话失效，重新登录
    messages.success(request, '密码已修改，请使用新密码重新登录。')
    return redirect('login')


@login_required(login_url='login')
@require_POST
def app_settings_storage(request):
    """修改作品/数据存储位置。

    流程：校验目标目录 -> 复制数据库与媒体 -> 写入引导指针 -> 提示重启。
    """
    from django.conf import settings as dj_settings
    from . import app_config

    new_dir = request.POST.get('data_dir', '').strip().strip('"')
    if not new_dir:
        messages.error(request, '请输入有效的存储目录。')
        return redirect('app_settings')

    try:
        target = __import__('pathlib').Path(new_dir)
        target.mkdir(parents=True, exist_ok=True)
        # 可写性测试
        (target / '.write_test').write_text('ok', encoding='utf-8')
        (target / '.write_test').unlink()
    except OSError:
        messages.error(request, '目标目录不可写，请更换位置。')
        return redirect('app_settings')

    old_dir = dj_settings.DATA_DIR
    try:
        app_config.migrate_data(old_dir, target)
        app_config.set_data_dir_pointer(str(target))
    except OSError as exc:
        messages.error(request, f'迁移数据失败：{exc}')
        return redirect('app_settings')

    messages.success(
        request,
        f'存储位置已更改并完成数据迁移。新位置：{target}。请关闭并重新启动应用以生效。'
    )
    return redirect('app_settings')
