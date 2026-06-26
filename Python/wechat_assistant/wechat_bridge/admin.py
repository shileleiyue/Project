from django.contrib import admin
from .models import WeChatAccount, SyncLog


@admin.register(WeChatAccount)
class WeChatAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'status', 'is_active', 'updated_at']
    list_filter = ['platform', 'status', 'is_active']


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['account', 'sync_type', 'status', 'started_at', 'finished_at']
    list_filter = ['status', 'sync_type']