from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    def _base_queryset(self):
        return super().get_queryset()# 获取基础查询集，不过滤已删除项
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)  # 默认过滤已删除项

    def delete(self):
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()
    def active(self):
        return self.filter(is_deleted=False)
    
    def deleted(self):
        return self.filter(is_deleted=True)

class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name='作品名称')               # 作品名称
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(blank=True, verbose_name='作品简介')
    cover_image = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='封面图路径'
    )   
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')                                             # 封面图路径

    objects = SoftDeleteQuerySet.as_manager()  # 使用软删除查询集管理器

    class Meta:
        verbose_name = '作品'
        verbose_name_plural = '作品管理'

    def __str__(self):
        return self.title
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields= ['is_deleted'])
        self.chapters.all().update(is_deleted=True)  # 级联软删除章节


class Chapter(models.Model):
    title = models.CharField(max_length=200,verbose_name='章节标题')               # 章节标题
    content = models.TextField(blank=True, verbose_name='正文内容')                 # 正文内容
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')   # 创建时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')       # 最后修改时间
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='所属作品'
    )                                                      # 所属作品
    event_refs = models.JSONField(blank=True, null=True, verbose_name='事件关联')   # 事件关联预留
    tech_refs = models.JSONField(blank=True, null=True, verbose_name='科技关联')    # 科技关联预留
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')                                             # 是否已删除

    objects = SoftDeleteQuerySet.as_manager()  # 使用软删除查询集管理器
    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节管理'

    def __str__(self):
        return f"{self.work.title} - {self.title}"
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields= ['is_deleted'])# 章节软删除

