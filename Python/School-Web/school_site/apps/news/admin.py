from django.contrib import admin
from .models import NewsCategory, Article


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category_type']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'pub_date', 'is_pinned']
    list_filter = ['category', 'is_pinned']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'pub_date'
    autocomplete_fields = ['cover_image']  # 方便选择封面图片