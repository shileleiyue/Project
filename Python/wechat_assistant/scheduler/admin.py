from django.contrib import admin
from .models import Schedule, Todo


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'status', 'location']
    list_filter = ['status', 'start_time']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_time'


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_done', 'due_date', 'created_at']
    list_filter = ['priority', 'is_done', 'due_date']
    search_fields = ['title']