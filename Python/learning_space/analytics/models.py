from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class WeakKP(models.Model):
    """薄弱知识点（根据错题自动更新）"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weak_kps')
    kp = models.ForeignKey('courses.KnowledgePoint', on_delete=models.CASCADE, related_name='weak_by')
    wrong_count = models.IntegerField(default=0)
    mastery_level = models.FloatField(default=50, verbose_name='掌握度 0-100')
    last_wrong_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('student', 'kp')]
        ordering = ['-wrong_count']
        verbose_name = '薄弱知识点'
        verbose_name_plural = '薄弱知识点'


class DailyStat(models.Model):
    """每日学习统计快照"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_stats')
    stat_date = models.DateField()
    total_duration_seconds = models.IntegerField(default=0, verbose_name='学习总时长（秒）')
    materials_count = models.IntegerField(default=0, verbose_name='学习资料数')
    kps_count = models.IntegerField(default=0, verbose_name='涉及知识点数')
    avg_effective_rate = models.FloatField(default=0, verbose_name='平均有效率（完成/开始）')

    class Meta:
        unique_together = [('student', 'stat_date')]
        ordering = ['-stat_date']
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'


class LearningPreference(models.Model):
    """学习喜好"""
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_preference')
    preferred_material_type = models.CharField(max_length=16, blank=True, default='')
    active_hours = models.JSONField(default=dict, verbose_name='活跃时段分布 {"20":0.9, ...}')
    subject_weights = models.JSONField(default=dict, verbose_name='主题权重 {"高等数学":0.8, ...}')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '学习喜好'
        verbose_name_plural = '学习喜好'


class Recommendation(models.Model):
    """推荐学习资料"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    material = models.ForeignKey('materials.Material', on_delete=models.CASCADE, related_name='recommended_for')
    reason = models.CharField(max_length=200, default='', verbose_name='推荐理由')
    score = models.FloatField(default=0)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name = '推荐'
        verbose_name_plural = '推荐'
