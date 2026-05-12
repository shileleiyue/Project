from django.shortcuts import render
from .models import SchoolInfo
from apps.news.models import Article  # 后面开发 news 时会用到


def home(request):
    # 获取学校基本信息（若未创建，返回 None）
    school_info = SchoolInfo.objects.first()
    
    # 获取最新新闻（暂时为空列表，等 news 应用完成后再取消注释）
    latest_news = Article.objects.filter(category__category_type='news').order_by('-pub_date')[:6]
    
    context = {
        'school_info': school_info,
        'latest_news': latest_news,
    }
    return render(request, 'core/home.html', context)