from django.contrib import admin
from .models import AdmissionBrochure, Job, ZhongKaoFAQ


@admin.register(AdmissionBrochure)
class AdmissionBrochureAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'is_active']
    list_filter = ['is_active']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'is_active']
    list_filter = ['is_active']


@admin.register(ZhongKaoFAQ)
class ZhongKaoFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order']