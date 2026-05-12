from django.db import models
from django.utils.translation import gettext_lazy as _


class FlatPage(models.Model):
    """
    固定单页：学校概况、历史沿革、办学理念、校园风光等。
    通过 slug 作为 URL 访问。
    """
    PAGE_TYPE_CHOICES = [
        ('about', _('学校概况')),
        ('history', _('历史沿革')),
        ('philosophy', _('办学理念')),
        ('campus', _('校园风光')),
        ('custom', _('自定义页面')),
    ]

    title = models.CharField(_('标题'), max_length=100)
    slug = models.SlugField(_('URL 别名'), unique=True)
    content = models.TextField(_('内容'), help_text='支持 HTML')
    page_type = models.CharField(
        _('页面类型'), max_length=20,
        choices=PAGE_TYPE_CHOICES,
        default='custom'
    )
    is_published = models.BooleanField(_('发布'), default=True)

    class Meta:
        verbose_name = _('固定单页')
        verbose_name_plural = _('固定单页')

    def __str__(self):
        return self.title