from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.gallery.models import FlowImage


class ClassRoom(models.Model):
    """班级"""
    GRADE_CHOICES = [(str(i), f'{i}年级') for i in range(7, 13)]  # 初一~高三

    name = models.CharField(_('班级名称'), max_length=50, unique=True)
    grade = models.CharField(_('年级'), max_length=2, choices=GRADE_CHOICES)
    year = models.PositiveSmallIntegerField(_('入学年份'), help_text='如 2023')
    is_active = models.BooleanField(_('当前有效'), default=True)

    class Meta:
        verbose_name = _('班级')
        verbose_name_plural = _('班级')
        ordering = ['grade', 'name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """自定义用户模型"""
    ROLE_CHOICES = [
        ('student', _('学生')),
        ('parent', _('家长')),
        ('teacher', _('教师')),
        ('head_teacher', _('班主任')),
        ('academic_director', _('教务主任')),
        ('principal', _('校长')),
        ('counselor', _('辅导员')),
        ('staff', _('后勤/行政')),
        ('whiteboard', _('班级账户')),
        ('admin', _('管理员')),
    ]

    role = models.CharField(_('角色'), max_length=20, choices=ROLE_CHOICES, default='student')
    real_name = models.CharField(_('真实姓名'), max_length=50, blank=True)
    student_id = models.CharField(_('学号/工号'), max_length=30, blank=True, unique=True, null=True)
    phone = models.CharField(_('手机号'), max_length=20, blank=True)
    avatar = models.ForeignKey(
        FlowImage, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='user_avatars', verbose_name=_('头像')
    )

    # 班级关联（学生和班级账户必填）
    classroom = models.ForeignKey(
        ClassRoom, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='members', verbose_name=_('所属班级')
    )

    # 班级账户专用
    is_whiteboard = models.BooleanField(_('是否为班级账户'), default=False)
    whiteboard_token = models.CharField(_('长期令牌'), max_length=255, blank=True, null=True, unique=True)
    token_expiry = models.DateTimeField(_('令牌过期时间'), null=True, blank=True)

    # 家长专用（绑定学生）
    children = models.ManyToManyField(
        'self', blank=True, symmetrical=False,
        limit_choices_to={'role': 'student'},
        related_name='parents',
        verbose_name=_('关联孩子')
    )

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return f'{self.real_name or self.username} ({self.get_role_display()})'