from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.validators import validate_file_extension, validate_file_size


class AdmissionBrochure(models.Model):
    """招生简章"""
    title = models.CharField(_('标题'), max_length=200)
    content = models.TextField(_('内容'), blank=True, help_text='可直接填写或留空仅上传文件')
    pdf_file = models.FileField(
        _('PDF文件'),
        upload_to='admissions/brochures/',
        blank=True,
        validators=[
            validate_file_extension(['pdf']),
            validate_file_size(10)
        ]
    )
    pub_date = models.DateTimeField(_('发布时间'), auto_now_add=True)
    is_active = models.BooleanField(_('当前有效'), default=True)

    class Meta:
        verbose_name = _('招生简章')
        verbose_name_plural = _('招生简章')
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Job(models.Model):
    """教师招聘"""
    title = models.CharField(_('岗位名称'), max_length=100)
    description = models.TextField(_('岗位描述'))
    requirements = models.TextField(_('任职要求'), blank=True)
    pub_date = models.DateTimeField(_('发布时间'), auto_now_add=True)
    is_active = models.BooleanField(_('正在招聘'), default=True)

    class Meta:
        verbose_name = _('招聘岗位')
        verbose_name_plural = _('招聘岗位')
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class ZhongKaoFAQ(models.Model):
    """中考咨询"""
    question = models.CharField(_('问题'), max_length=200)
    answer = models.TextField(_('回答'))
    order = models.PositiveSmallIntegerField(_('排序'), default=0)

    class Meta:
        verbose_name = _('中考咨询')
        verbose_name_plural = _('中考咨询')
        ordering = ['order']

    def __str__(self):
        return self.question