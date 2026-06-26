from django.contrib import admin
from .models import Graduate


@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ['name', 'graduate_year', 'achievement', 'order']
    autocomplete_fields = ['photo']