from django.db import models

# Create your models here.
from django.db import models

class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name='作品名称')               # 作品名称
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(blank=True, verbose_name='作品简介')
    cover_image = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='封面图路径'
    )                                                # 封面图路径

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=200,verbose_name='')               # 章节标题
    content = models.TextField(blank=True)                 # 正文内容
    created_at = models.DateTimeField(auto_now_add=True)   # 创建时间
    updated_at = models.DateTimeField(auto_now=True)       # 最后修改时间
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='chapters'
    )                                                      # 所属作品
    event_refs = models.JSONField(blank=True, null=True)   # 事件关联预留
    tech_refs = models.JSONField(blank=True, null=True)    # 科技关联预留

    def __str__(self):
        return f"{self.work.title} - {self.title}"