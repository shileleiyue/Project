from django.db import models
from django.conf import settings
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
    
class SoftDeleteManager(models.Manager):
    """自定义管理器，确保默认只查询未删除的记录"""

    def get_queryset(self):
        # 关键：返回一个已经过滤好的 SoftDeleteQuerySet
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    # 暴露其他自定义方法
    def deleted(self):
        """返回所有已删除记录的 QuerySet"""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)

    def active(self):
        """返回未删除记录的 QuerySet（与默认相同）"""
        return self.get_queryset()

    def hard_delete(self):
        """彻底删除（谨慎使用）"""
        return SoftDeleteQuerySet(self.model, using=self._db).hard_delete()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类管理'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签管理'

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name='作品名称')               # 作品名称
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(blank=True, verbose_name='作品简介')
    cover_image = models.ImageField(
        max_length=200,
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name='封面图'
    )   
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')                                             # 封面图路径
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='works', verbose_name='创作者', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类', related_name='works')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签', related_name='works')

    objects = SoftDeleteManager()  # 使用软删除管理器

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
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')      # 是否已删除
    order = models.IntegerField(default=0, verbose_name='排序序号')

    objects = SoftDeleteManager()  # 使用软删除管理器
    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节管理'
        ordering = ['order', 'created_at']  # 默认排序：先按order升序，再按created_at升序

    def __str__(self):
        return f"{self.work.title} - {self.title}"
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields= ['is_deleted'])# 章节软删除
    outline = models.ForeignKey(
        'OutlineNode',
        on_delete=models.SET_NULL,
        related_name='chapters',
        verbose_name='所属大纲节点',
        blank=True,
        null=True,
    )  # 关联大纲节点

class OutlineNode(models.Model):
    title = models.CharField(max_length=200, verbose_name='大纲节点标题')  # 大纲节点标题
    content = models.TextField(blank=True, verbose_name='大纲内容')  # 大纲内容
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')  # 最后修改时间
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='outline_nodes',
        verbose_name='所属作品'
    )  # 所属作品
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',verbose_name='父节点',
        blank=True,
        null=True,
    )  # 父节点
    order = models.IntegerField(default=0, verbose_name='排序序号')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除') 
    objects = SoftDeleteQuerySet.as_manager()  # 使用软删除查询集管理器

    class Meta:
        verbose_name = '大纲节点'
        verbose_name_plural = '大纲节点管理'
        ordering = ['order', 'created_at']  # 默认排序：先按order升序，再按created_at升序
    def __str__(self):
        return f"{self.work.title} - {self.title}"
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields= ['is_deleted'])# 大纲节点软删除
        self.children.all().update(is_deleted=True)  # 级联软删除子节点

class DailyStats(models.Model):
    """每日创作统计"""
    date = models.DateField(unique=True, verbose_name='日期')
    word_count = models.IntegerField(default=0, verbose_name='码字数')          # 当日新增字数
    duration_seconds = models.IntegerField(default=0, verbose_name='创作时长(秒)')
    last_update = models.DateTimeField(auto_now=True, verbose_name='最后更新')

    class Meta:
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'

    def __str__(self):
        return f"{self.date} - {self.word_count}字 / {self.duration_seconds//60}分钟"


class Character(models.Model):
    name = models.CharField(max_length=80, verbose_name='姓名')
    alias = models.CharField(max_length=80, blank=True, verbose_name='别名')
    gender = models.CharField(max_length=10, blank=True, verbose_name='性别')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
    description = models.TextField(blank=True, verbose_name='描述')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='characters', verbose_name='所属作品', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])


class Relationship(models.Model):
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='relationships_as_char1', verbose_name='角色A')
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='relationships_as_char2', verbose_name='角色B')
    relation_type = models.CharField(max_length=50, verbose_name='关系类型')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '角色关系'
        verbose_name_plural = '角色关系管理'

    def __str__(self):
        return f"{self.character1} - {self.character2} : {self.relation_type}"


class TimelineEvent(models.Model):
    title = models.CharField(max_length=100, verbose_name='事件标题')
    date = models.CharField(max_length=20, blank=True, verbose_name='日期')
    description = models.TextField(blank=True, verbose_name='描述')
    characters = models.ManyToManyField(Character, related_name='timeline_events', blank=True, verbose_name='关联角色')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='timeline_events', verbose_name='所属作品', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '时间线事件'
        verbose_name_plural = '时间线事件管理'

    def __str__(self):
        return self.title


class TechNode(models.Model):
    name = models.CharField(max_length=100, verbose_name='节点名称')
    description = models.TextField(blank=True, verbose_name='描述')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name='父节点')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='tech_nodes', verbose_name='所属作品', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '科技树节点'
        verbose_name_plural = '科技树节点管理'

    def __str__(self):
        return self.name

class WritingGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writing_goals', verbose_name='用户')
    daily_goal = models.IntegerField(default=1000, verbose_name='每日目标字数')
    weekly_goal = models.IntegerField(default=7000, verbose_name='每周目标字数')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新')

    class Meta:
        verbose_name = '写作目标'
        verbose_name_plural = '写作目标管理'

    def __str__(self):
        return f"{self.user.username}: 每日{self.daily_goal}字/每周{self.weekly_goal}字"