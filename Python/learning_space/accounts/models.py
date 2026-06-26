from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.TextChoices):
    ADMIN = 'admin', '管理员'
    TEACHER = 'teacher', '教师'
    STUDENT = 'student', '学生'


class UserManager(BaseUserManager):
    """自定义 User 管理器"""
    def create_user(self, username, password=None, role=Role.STUDENT, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    """扩展用户模型"""
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.STUDENT, verbose_name='角色')
    email = models.EmailField(blank=True, default='', verbose_name='邮箱')
    phone = models.CharField(max_length=32, blank=True, default='', verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')

    objects = UserManager()

    def __str__(self):
        name = self.get_full_name() or self.username
        return f'[{self.role}] {name}'

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    @property
    def is_teacher(self):
        return self.role == Role.TEACHER

    @property
    def is_student(self):
        return self.role == Role.STUDENT


class Student(models.Model):
    """学生扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', verbose_name='账号')
    student_no = models.CharField(max_length=32, unique=True, verbose_name='学号')
    name = models.CharField(max_length=64, verbose_name='姓名')
    college = models.CharField(max_length=128, blank=True, default='', verbose_name='学院')
    major = models.CharField(max_length=128, blank=True, default='', verbose_name='专业')
    grade = models.CharField(max_length=16, blank=True, default='', verbose_name='年级')
    contact = models.CharField(max_length=128, blank=True, default='', verbose_name='联系方式')

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'
        ordering = ['student_no']

    def __str__(self):
        return f'{self.student_no} - {self.name}'


class Teacher(models.Model):
    """教师扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', verbose_name='账号')
    teacher_no = models.CharField(max_length=32, unique=True, verbose_name='教师编号')
    name = models.CharField(max_length=64, verbose_name='姓名')
    title = models.CharField(max_length=64, blank=True, default='', verbose_name='职称')
    department = models.CharField(max_length=128, blank=True, default='', verbose_name='院系')
    contact = models.CharField(max_length=128, blank=True, default='', verbose_name='联系方式')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return f'{self.teacher_no} - {self.name}'


class StudentCourse(models.Model):
    """学生-课程-成绩 关联"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_scores', verbose_name='学生')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='student_scores', verbose_name='课程')
    score = models.FloatField(null=True, blank=True, verbose_name='成绩')
    semester = models.CharField(max_length=16, blank=True, default='', verbose_name='学期（如 2025-2026-1）')
    enrolled_at = models.DateField(auto_now_add=True, verbose_name='选课日期')

    class Meta:
        verbose_name = '学生成绩'
        verbose_name_plural = '学生成绩'
        unique_together = [('student', 'course')]  # 一个学生同一课程一条记录

    def __str__(self):
        return f'{self.student.name} - {self.course.name} - {self.score or "未考"}'
