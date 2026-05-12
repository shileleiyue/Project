from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.gallery.models import FlowImage


class NewsCategory(models.Model):
    """新闻分类：新闻、通知、媒体报道等"""
    CATEGORY_TYPE_CHOICES = [
        ('news', _('新闻动态')),
        ('notice', _('通知公告')),
        ('media_report', _('媒体报道')),
    ]
    name = models.CharField(_('分类名称'), max_length=50)
    slug = models.SlugField(_('URL 别名'), unique=True)
    category_type = models.CharField(
        _('分类类型'), max_length=20,
        choices=CATEGORY_TYPE_CHOICES,
        default='news'
    )

    class Meta:
        verbose_name = _('新闻分类')
        verbose_name_plural = _('新闻分类')

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章：新闻、通知、媒体报道"""
    title = models.CharField(_('标题'), max_length=200)
    slug = models.SlugField(_('URL 别名'), unique=True)
    content = models.TextField(_('内容'))
    excerpt = models.TextField(_('摘要'), blank=True, help_text='用于列表展示，不填则自动截取正文前200字')
    pub_date = models.DateTimeField(_('发布时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE,
        related_name='articles', verbose_name=_('分类')
    )
    cover_image = models.ForeignKey(
        FlowImage, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='articles',
        verbose_name=_('封面图片')
    )
    is_pinned = models.BooleanField(_('置顶'), default=False)

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['-is_pinned', '-pub_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = Truncator(self.content).chars(200, html=True)
        super().save(*args, **kwargs)