from django.db import models
from django.utils.translation import gettext_lazy as _


class SchoolInfo(models.Model):
    """
    学校基础信息表，通常只有一条记录。
    用于存储全局使用的校名、简介、联系方式等。
    """
    name = models.CharField(_('学校全称'), max_length=100)
    short_name = models.CharField(_('简称'), max_length=30, blank=True)
    logo_usage = models.CharField(
        _('Logo 用途标识'),
        max_length=50,
        default='logo',
        help_text='对应 gallery_staticimage 表中的 usage 字段，用于调用本地图片库中的 Logo'
    )
    brief_intro = models.TextField(_('一句话简介'), max_length=500, blank=True)
    about = models.TextField(_('学校概况'), blank=True)
    history = models.TextField(_('历史沿革'), blank=True)
    philosophy = models.TextField(_('办学理念'), blank=True)
    address = models.CharField(_('地址'), max_length=255, blank=True)
    phone = models.CharField(_('电话'), max_length=20, blank=True)
    email = models.EmailField(_('邮箱'), blank=True)
    website = models.URLField(_('官网地址'), blank=True)

    class Meta:
        verbose_name = _('学校信息')
        verbose_name_plural = _('学校信息')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 确保只有一条记录
        if not self.pk and SchoolInfo.objects.exists():
            raise ValueError('只能有一条学校信息记录，请修改已有的记录。')
        super().save(*args, **kwargs)