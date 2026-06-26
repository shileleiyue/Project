# 1. 导入 admin 模块（通常已自动存在于 admin.py）
from django.contrib import admin

# 2. 导入你需要管理的模型（Work）
from .models import Work, Chapter, OutlineNode, DailyStats, WritingGoal, Character, Relationship, TimelineEvent, TechNode, Category, Tag

# Register your models here.
admin.site.register(Work)
admin.site.register(Chapter)
admin.site.register(OutlineNode)
admin.site.register(DailyStats)
admin.site.register(WritingGoal)
admin.site.register(Character)
admin.site.register(Relationship)
admin.site.register(TimelineEvent)
admin.site.register(TechNode)
admin.site.register(Category)
admin.site.register(Tag)