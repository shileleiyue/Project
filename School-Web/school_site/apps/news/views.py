from django.shortcuts import render, get_object_or_404
from .models import Article, NewsCategory


def article_list(request, category_slug=None):
    """文章列表页，可按分类过滤"""
    categories = NewsCategory.objects.all()
    
    if category_slug:
        category = get_object_or_404(NewsCategory, slug=category_slug)
        articles = Article.objects.filter(category=category)
        title = category.name
    else:
        category = None
        articles = Article.objects.all()
        title = '新闻中心'

    # 置顶文章优先显示
    articles = articles.order_by('-is_pinned', '-pub_date')

    context = {
        'articles': articles,
        'categories': categories,
        'current_category': category,
        'title': title,
    }
    return render(request, 'news/article_list.html', context)


def article_detail(request, slug):
    """文章详情页"""
    article = get_object_or_404(Article, slug=slug)
    # 侧边栏推荐：同分类的其他文章
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(id=article.id).order_by('-pub_date')[:5]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'news/article_detail.html', context)