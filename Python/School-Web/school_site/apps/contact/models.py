from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    """留言板"""
    sender_name = models.CharField(_('姓名'), max_length=50)
    email = models.EmailField(_('邮箱'), blank=True)
    content = models.TextField(_('留言内容'))
    sent_at = models.DateTimeField(_('发送时间'), auto_now_add=True)
    is_public = models.BooleanField(_('公开显示'), default=True)

    class Meta:
        verbose_name = _('留言板')
        verbose_name_plural = _('留言板')
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.sender_name} 的留言'


class PrincipalMail(models.Model):
    """校长信箱"""
    sender_name = models.CharField(_('姓名'), max_length=50)
    email = models.EmailField(_('邮箱'))
    subject = models.CharField(_('主题'), max_length=100)
    content = models.TextField(_('内容'))
    sent_at = models.DateTimeField(_('发送时间'), auto_now_add=True)
    is_read = models.BooleanField(_('已读'), default=False)

    class Meta:
        verbose_name = _('校长信箱')
        verbose_name_plural = _('校长信箱')
        ordering = ['-sent_at']

    def __str__(self):
        return self.subject