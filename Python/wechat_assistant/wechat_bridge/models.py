from django.db import models


class WeChatAccount(models.Model):
    PLATFORM_CHOICES = [
        ('wechat_work', '企业微信'),
        ('personal', '个人微信'),
        ('official_account', '微信公众号'),
    ]

    STATUS_CHOICES = [
        ('online', '在线'),
        ('offline', '离线'),
        ('error', '异常'),
    ]

    name = models.CharField(max_length=100, verbose_name='账户名称')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='平台类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', verbose_name='状态')
    config = models.JSONField(default=dict, blank=True, verbose_name='配置信息')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '微信账户'
        verbose_name_plural = '微信账户'

    def __str__(self):
        return f'{self.name} ({self.get_platform_display()})'


class SyncLog(models.Model):
    account = models.ForeignKey(WeChatAccount, on_delete=models.CASCADE, related_name='sync_logs', verbose_name='账户')
    sync_type = models.CharField(max_length=50, verbose_name='同步类型')
    status = models.CharField(max_length=20, choices=[('success', '成功'), ('failed', '失败'), ('running', '进行中')], verbose_name='状态')
    message = models.TextField(blank=True, verbose_name='日志信息')
    started_at = models.DateTimeField(verbose_name='开始时间')
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '同步日志'
        verbose_name_plural = '同步日志'
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.account.name} - {self.sync_type} - {self.get_status_display()}'