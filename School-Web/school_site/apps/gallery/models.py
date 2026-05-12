from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.validators import validate_file_extension, validate_file_size


class StaticImage(models.Model):
    title = models.CharField(_('标题'), max_length=100)
    image_path = models.CharField(
        _('图片路径'), max_length=255,
        help_text='相对于 static/gallery/ 的路径，例如 "logo.png"'
    )
    usage = models.CharField(_('用途'), max_length=50, unique=True)
    description = models.CharField(_('描述'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('本地图片')
        verbose_name_plural = _('本地图片')

    def __str__(self):
        return f'{self.usage} - {self.title}'


class FlowAlbum(models.Model):
    name = models.CharField(_('相册名称'), max_length=100)
    slug = models.SlugField(_('URL 别名'), unique=True)
    cover_image = models.ForeignKey(
        'FlowImage', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cover_of_album',
        verbose_name=_('封面图片')
    )
    description = models.TextField(_('描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('流动相册')
        verbose_name_plural = _('流动相册')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class FlowImage(models.Model):
    album = models.ForeignKey(
        FlowAlbum, on_delete=models.CASCADE,
        related_name='images', verbose_name=_('所属相册')
    )
    image = models.ImageField(
        _('图片文件'),
        upload_to='gallery/albums/%Y/%m/',
        validators=[validate_file_size(5)]  # 限制 5MB
    )
    caption = models.CharField(_('标题/说明'), max_length=200, blank=True)
    uploaded_at = models.DateTimeField(_('上传时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('流动图片')
        verbose_name_plural = _('流动图片')
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.album.name} - {self.caption or self.image.name}'


class Video(models.Model):
    title = models.CharField(_('标题'), max_length=200)
    video_url = models.URLField(_('视频链接'), blank=True)
    video_file = models.FileField(
        _('视频文件'),
        upload_to='gallery/videos/%Y/%m/',
        blank=True,
        validators=[
            validate_file_extension(['mp4', 'webm', 'ogg']),
            validate_file_size(20)
        ]
    )
    thumbnail = models.ImageField(
        _('封面缩略图'),
        upload_to='gallery/videos/thumbnails/',
        blank=True
    )
    album = models.ForeignKey(
        FlowAlbum, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='videos',
        verbose_name=_('所属相册（可选）')
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('视频')
        verbose_name_plural = _('视频')
        ordering = ['-created_at']

    def __str__(self):
        return self.title