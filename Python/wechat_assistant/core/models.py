from django.db import models


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('personal', '个人'),
        ('group', '群组'),
        ('official', '公众号'),
    ]

    wx_id = models.CharField(max_length=100, unique=True, verbose_name='微信ID')
    name = models.CharField(max_length=200, verbose_name='昵称')
    remark = models.CharField(max_length=200, blank=True, verbose_name='备注名')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='personal', verbose_name='类型')
    avatar = models.URLField(blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = '联系人'
        ordering = ['-updated_at']

    def __str__(self):
        return self.remark or self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    color = models.CharField(max_length=20, default='#1890ff', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', '文本'),
        ('image', '图片'),
        ('file', '文件'),
        ('link', '链接'),
        ('system', '系统消息'),
    ]

    msg_id = models.CharField(max_length=100, unique=True, verbose_name='消息ID')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages', verbose_name='联系人')
    msg_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text', verbose_name='消息类型')
    content = models.TextField(blank=True, verbose_name='消息内容')
    timestamp = models.DateTimeField(verbose_name='消息时间')
    is_starred = models.BooleanField(default=False, verbose_name='是否星标')
    tags = models.ManyToManyField(Tag, blank=True, related_name='messages', verbose_name='标签')
    is_from_self = models.BooleanField(default=True, verbose_name='是否自己发送')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['contact', 'timestamp']),
        ]

    def __str__(self):
        return f'{self.contact.name}: {self.content[:50]}'


class Conversation(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='conversations', verbose_name='联系人')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name='最后一条消息')
    unread_count = models.IntegerField(default=0, verbose_name='未读数')
    is_archived = models.BooleanField(default=False, verbose_name='是否归档')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '会话'
        verbose_name_plural = '会话'
        ordering = ['-updated_at']

    def __str__(self):
        return f'会话: {self.contact.name}'