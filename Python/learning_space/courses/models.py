from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """课程"""
    code = models.CharField(max_length=64, unique=True, verbose_name='课程代码')
    name = models.CharField(max_length=128, verbose_name='课程名')
    description = models.TextField(blank=True, default='', verbose_name='课程简介')
    cover = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name='封面')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='taught_courses', verbose_name='授课教师')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.code}] {self.name}'


class KnowledgePoint(models.Model):
    """知识点（支持树形结构）"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='knowledge_points', verbose_name='课程')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='父知识点')
    title = models.CharField(max_length=128, verbose_name='知识点标题')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    order_no = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        verbose_name = '知识点'
        verbose_name_plural = '知识点'
        ordering = ['course', 'parent_id', 'order_no', 'id']
        unique_together = [('course', 'parent', 'order_no', 'title')]

    def __str__(self):
        prefix = f'{self.parent.title} / ' if self.parent else ''
        return f'{prefix}{self.title}'

    def get_ancestors(self):
        """获取所有祖先"""
        ancestors = []
        cur = self.parent
        while cur:
            ancestors.insert(0, cur)
            cur = cur.parent
        return ancestors
