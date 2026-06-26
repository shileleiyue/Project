from django.contrib import admin
from .models import Message, PrincipalMail


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'email', 'sent_at', 'is_public']
    list_filter = ['is_public']


@admin.register(PrincipalMail)
class PrincipalMailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender_name', 'sent_at', 'is_read']
    list_filter = ['is_read']