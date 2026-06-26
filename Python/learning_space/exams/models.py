from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    """题目（单选/多选/判断）"""
    class Type(models.TextChoices):
        SINGLE = 'single', '单选题'
        MULTI = 'multi', '多选题'
        JUDGE = 'judge', '判断题'

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='questions', verbose_name='课程')
    kp = models.ForeignKey('courses.KnowledgePoint', on_delete=models.SET_NULL,
                           null=True, blank=True, related_name='questions', verbose_name='知识点')
    question_type = models.CharField(max_length=16, choices=Type.choices, verbose_name='题型')
    title = models.TextField(verbose_name='题干')
    options = models.JSONField(default=dict, verbose_name='选项（JSON：{"A":"...","B":"..."}）')
    correct_answer = models.JSONField(verbose_name='正确答案（JSON：单选存"A"；多选存["A","C"]；判断存true/false）')
    analysis = models.TextField(blank=True, default='', verbose_name='解析')
    difficulty = models.PositiveSmallIntegerField(default=3, verbose_name='难度 1-5')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='questions', verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_question_type_display()}] {self.title[:40]}'


class Exam(models.Model):
    """试卷"""
    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PUBLISHED = 'published', '已发布'

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='exams', verbose_name='课程')
    title = models.CharField(max_length=200, verbose_name='试卷名称')
    description = models.TextField(blank=True, default='', verbose_name='说明')
    duration_minutes = models.IntegerField(default=30, verbose_name='考试时长（分钟）')
    passing_score = models.FloatField(default=60, verbose_name='及格分数')
    total_score = models.FloatField(default=100, verbose_name='满分')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='exams', verbose_name='出题人')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.items.count()


class ExamQuestion(models.Model):
    """试卷-题目关联"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='items')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='exam_items')
    score = models.FloatField(default=5, verbose_name='本题分值')
    order_no = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        ordering = ['order_no', 'id']
        unique_together = [('exam', 'question')]


class ExamRecord(models.Model):
    """考试记录"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_records')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True, verbose_name='最终得分')
    is_passed = models.BooleanField(null=True, blank=True, verbose_name='是否及格')

    class Meta:
        ordering = ['-started_at']
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录'

    def __str__(self):
        return f'{self.student} - {self.exam} - {self.score}'


class ExamAnswer(models.Model):
    """每道题的作答"""
    record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.JSONField(null=True, blank=True, verbose_name='学生答案')
    is_correct = models.BooleanField(null=True, blank=True)
    score_obtained = models.FloatField(default=0)

    class Meta:
        ordering = ['id']
