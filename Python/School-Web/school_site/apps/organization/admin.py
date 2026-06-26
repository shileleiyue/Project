from django.contrib import admin
from .models import Department, Leader, Teacher


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order']
    autocomplete_fields = ['photo']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'department', 'order']
    list_filter = ['department']
    autocomplete_fields = ['photo']