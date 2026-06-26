from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import SchoolInfo
from apps.news.models import Article, NewsCategory
from apps.pages.models import FlatPage
from apps.organization.models import Department, Teacher


def home(request):
    school_info = SchoolInfo.objects.first()
    latest_news = Article.objects.filter(category__category_type='news').order_by('-pub_date')[:6]
    context = {
        'school_info': school_info,
        'latest_news': latest_news,
    }
    return render(request, 'core/home.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    articles = []
    flatpages = []
    teachers = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).order_by('-pub_date')

        flatpages = FlatPage.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        teachers = Teacher.objects.filter(
            Q(name__icontains=query) |
            Q(title__icontains=query) |
            Q(intro__icontains=query)
        ).order_by('name')

    total_results = len(articles) + len(flatpages) + len(teachers)

    context = {
        'query': query,
        'articles': articles,
        'flatpages': flatpages,
        'teachers': teachers,
        'total_results': total_results,
    }
    return render(request, 'core/search_results.html', context)


def sitemap_view(request):
    pages = []

    pages.append({
        'name': '首页',
        'url': reverse('core:home'),
        'children': None,
    })

    pages.append({
        'name': '学校概况',
        'url': None,
        'children': [
            {'name': '学校简介', 'url': reverse('pages:about')},
            {'name': '历史沿革', 'url': reverse('pages:school_history')},
            {'name': '校园文化', 'url': reverse('pages:campus_culture')},
            {'name': '办学理念', 'url': reverse('pages:education_philosophy')},
            {'name': '学校愿景', 'url': reverse('pages:school_vision')},
        ],
    })

    departments = Department.objects.all()
    dept_children = [{'name': '全部部门', 'url': reverse('organization:departments')}]
    for dept in departments:
        dept_children.append({
            'name': dept.name,
            'url': reverse('organization:department_detail', kwargs={'slug': dept.slug}),
        })
    dept_children.append({'name': '领导介绍', 'url': reverse('organization:leaders')})
    dept_children.append({'name': '师资队伍', 'url': reverse('organization:teachers')})

    pages.append({
        'name': '组织架构',
        'url': None,
        'children': dept_children,
    })

    categories = NewsCategory.objects.all()
    news_children = [{'name': '全部信息', 'url': reverse('news:article_list')}]
    for cat in categories:
        news_children.append({
            'name': cat.name,
            'url': reverse('news:category_list', kwargs={'category_slug': cat.slug}),
        })

    articles = Article.objects.filter(is_pinned=True).order_by('-pub_date')[:20]
    article_children = []
    for article in articles:
        article_children.append({
            'name': article.title,
            'url': reverse('news:article_detail', kwargs={'slug': article.slug}),
        })

    pages.append({
        'name': '信息发布',
        'url': None,
        'children': news_children + ([
            {'name': '置顶文章', 'url': None, 'children': article_children}
        ] if article_children else []),
    })

    pages.append({
        'name': '招生招聘',
        'url': None,
        'children': [
            {'name': '招生简章', 'url': reverse('admissions:brochures')},
            {'name': '招聘信息', 'url': reverse('admissions:jobs')},
            {'name': '中考问答', 'url': reverse('admissions:zhongkao_faq')},
        ],
    })

    pages.append({
        'name': '毕业生',
        'url': None,
        'children': [
            {'name': '毕业生列表', 'url': reverse('graduates:list')},
        ],
    })

    pages.append({
        'name': '校园风光',
        'url': None,
        'children': [
            {'name': '相册列表', 'url': reverse('gallery:album_list')},
            {'name': '视频列表', 'url': reverse('gallery:video_list')},
        ],
    })

    pages.append({
        'name': '互动交流',
        'url': None,
        'children': [
            {'name': '留言板', 'url': reverse('contact:message_list')},
            {'name': '校长信箱', 'url': reverse('contact:principal_mail')},
        ],
    })

    context = {
        'pages': pages,
    }
    return render(request, 'core/sitemap.html', context)