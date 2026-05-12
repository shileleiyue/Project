from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # /news/ 所有文章列表
    path('', views.article_list, name='article_list'),
    # /news/category/<slug>/ 按分类列表
    path('category/<slug:category_slug>/', views.article_list, name='category_list'),
    # /news/article/<slug>/ 文章详情
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]