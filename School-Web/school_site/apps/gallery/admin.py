from django.contrib import admin
from django.utils.html import format_html
from .models import StaticImage, FlowAlbum, FlowImage, Video


class FlowImageInline(admin.TabularInline):
    model = FlowImage
    extra = 1
    fields = ['image', 'caption', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(FlowAlbum)
class FlowAlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'cover_preview', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FlowImageInline]
    search_fields = ['name']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" />', obj.cover_image.image.url)
        return '-'
    cover_preview.short_description = '封面'


@admin.register(StaticImage)
class StaticImageAdmin(admin.ModelAdmin):
    list_display = ['usage', 'title', 'image_path', 'description']
    search_fields = ['usage', 'title']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_source', 'album', 'created_at']
    list_filter = ['album']

    def video_source(self, obj):
        return '链接' if obj.video_url else '本地上传'
    video_source.short_description = '视频来源'

@admin.register(FlowImage)
class FlowImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'album', 'uploaded_at']
    search_fields = ['caption']