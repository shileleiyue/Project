from django.shortcuts import render, get_object_or_404
from .models import FlatPage

TEMPLATE_MAP = {
    'about': 'pages/about.html',
    'school_history': 'pages/school_history.html',
    'campus_culture': 'pages/campus_culture.html',
    'education_philosophy': 'pages/education_philosophy.html',
    'school_vision': 'pages/school_vision.html',
}

PAGE_TYPE_TITLES = {
    'about': '学校简介',
    'school_history': '历史沿革',
    'campus_culture': '校园文化',
    'education_philosophy': '办学理念',
    'school_vision': '学校愿景',
}


def page_detail(request, slug=None, page_type=None):
    if page_type:
        page = FlatPage.objects.filter(page_type=page_type, is_published=True).first()
        if not page:
            # 数据库中暂无记录，构造占位页面对象
            page = FlatPage(
                page_type=page_type,
                title=PAGE_TYPE_TITLES.get(page_type, page_type),
                content='<p>内容正在编辑中，敬请期待…</p>',
            )
    else:
        page = get_object_or_404(FlatPage, slug=slug, is_published=True)
    template = TEMPLATE_MAP.get(page.page_type, 'pages/page_detail.html')
    context = {'page': page}
    return render(request, template, context)