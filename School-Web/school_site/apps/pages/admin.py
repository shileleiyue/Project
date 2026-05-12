from django.contrib import admin
from .models import FlatPage


@admin.register(FlatPage)
class FlatPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'page_type', 'is_published']
    list_filter = ['page_type', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']