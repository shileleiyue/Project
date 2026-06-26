from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClassRoom


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'real_name', 'role', 'classroom', 'is_whiteboard', 'is_active']
    list_filter = ['role', 'is_whiteboard', 'classroom', 'is_active']
    search_fields = ['username', 'real_name', 'student_id', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('role', 'real_name', 'student_id', 'phone', 'avatar', 'classroom', 'is_whiteboard', 'whiteboard_token', 'token_expiry', 'children')}),
    )


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'year', 'is_active']
    list_filter = ['grade', 'is_active']