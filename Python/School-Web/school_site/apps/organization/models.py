from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.gallery.models import FlowImage


class Department(models.Model):
    """部门设置"""
    name = models.CharField(_('部门名称'), max_length=50)
    slug = models.SlugField(_('URL 别名'), unique=True)
    description = models.TextField(_('部门描述'), blank=True)
    order = models.PositiveSmallIntegerField(_('排序'), default=0)

    class Meta:
        verbose_name = _('部门')
        verbose_name_plural = _('部门')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Leader(models.Model):
    """领导介绍"""
    name = models.CharField(_('姓名'), max_length=30)
    position = models.CharField(_('职务'), max_length=50)
    intro = models.TextField(_('简介'), blank=True)
    photo = models.ForeignKey(
        FlowImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leader_photos',
        verbose_name=_('照片')
    )
    order = models.PositiveSmallIntegerField(_('排序'), default=0)

    class Meta:
        verbose_name = _('领导')
        verbose_name_plural = _('领导')
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} - {self.position}'


class Teacher(models.Model):
    """师资队伍"""
    name = models.CharField(_('姓名'), max_length=30)
    title = models.CharField(_('职称'), max_length=50, blank=True)
    intro = models.TextField(_('简介'), blank=True)
    photo = models.ForeignKey(
        FlowImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teacher_photos',
        verbose_name=_('照片')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers',
        verbose_name=_('所属部门')
    )
    order = models.PositiveSmallIntegerField(_('排序'), default=0)

    class Meta:
        verbose_name = _('教师')
        verbose_name_plural = _('教师')
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} - {self.title or "教师"}'