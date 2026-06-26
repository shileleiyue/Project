from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.gallery.models import FlowImage


class Graduate(models.Model):
    """优秀毕业生"""
    name = models.CharField(_('姓名'), max_length=50)
    graduate_year = models.PositiveSmallIntegerField(_('毕业年份'))
    achievement = models.CharField(_('成就/去向'), max_length=200)
    story = models.TextField(_('成长故事'), blank=True)
    photo = models.ForeignKey(FlowImage, on_delete=models.SET_NULL, null=True, blank=True, related_name='graduate_photos', verbose_name=_('照片'))
    order = models.PositiveSmallIntegerField(_('排序'), default=0)

    class Meta:
        verbose_name = _('优秀毕业生')
        verbose_name_plural = _('优秀毕业生')
        ordering = ['order', '-graduate_year']

    def __str__(self):
        return f'{self.name} ({self.graduate_year}届)'