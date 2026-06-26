from django.db import models


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    title = models.CharField(max_length=200, verbose_name='事件标题')
    description = models.TextField(blank=True, verbose_name='描述')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    location = models.CharField(max_length=200, blank=True, verbose_name='地点')
    source_msg = models.ForeignKey('core.Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules', verbose_name='来源消息')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    reminder_minutes = models.IntegerField(default=30, verbose_name='提前提醒分钟数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '日程'
        verbose_name_plural = '日程'
        ordering = ['start_time']

    def __str__(self):
        return self.title


class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    title = models.CharField(max_length=200, verbose_name='待办内容')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    is_done = models.BooleanField(default=False, verbose_name='是否完成')
    due_date = models.DateTimeField(blank=True, null=True, verbose_name='截止日期')
    source_msg = models.ForeignKey('core.Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='todos', verbose_name='来源消息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '待办事项'
        verbose_name_plural = '待办事项'
        ordering = ['-priority', 'due_date']

    def __str__(self):
        return self.title