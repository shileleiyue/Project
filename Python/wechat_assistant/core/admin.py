from django.contrib import admin
from .models import Contact, Tag, Message, Conversation


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'remark', 'contact_type', 'wx_id', 'updated_at']
    list_filter = ['contact_type']
    search_fields = ['name', 'remark', 'wx_id']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['msg_id', 'contact', 'msg_type', 'is_starred', 'timestamp']
    list_filter = ['msg_type', 'is_starred', 'timestamp']
    search_fields = ['content', 'msg_id']
    date_hierarchy = 'timestamp'


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['contact', 'last_message', 'unread_count', 'is_archived', 'updated_at']
    list_filter = ['is_archived']