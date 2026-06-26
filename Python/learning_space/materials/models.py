from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Material(models.Model):
    """学习资料"""
    class Type(models.TextChoices):
        DOCUMENT = 'document', '文档'
        VIDEO = 'video', '视频'
        LINK = 'link', '外链'

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                                related_name='materials', verbose_name='课程')
    kp = models.ForeignKey('courses.KnowledgePoint', on_delete=models.SET_NULL,
                           null=True, blank=True, related_name='materials', verbose_name='知识点')
    title = models.CharField(max_length=200, verbose_name='标题')
    material_type = models.CharField(max_length=16, choices=Type.choices, verbose_name='资料类型')
    file = models.FileField(upload_to='materials/', null=True, blank=True, verbose_name='文件')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='外链 URL')
    duration = models.IntegerField(default=0, verbose_name='时长（秒，视频用）')
    description = models.TextField(blank=True, default='', verbose_name='内容简介/富文本')
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='uploaded_materials', verbose_name='上传者')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '学习资料'
        verbose_name_plural = '学习资料'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_material_type_display()}] {self.title}'


class MaterialView(models.Model):
    """学习记录（学生每次看/读一个资料记一笔）"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='views')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_views')
    progress_percent = models.FloatField(default=0, verbose_name='进度（0-100）')
    duration_seconds = models.IntegerField(default=0, verbose_name='本次学习时长（秒）')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False, verbose_name='是否学完')

    class Meta:
        verbose_name = '学习记录'
        verbose_name_plural = '学习记录'
        ordering = ['-started_at']
