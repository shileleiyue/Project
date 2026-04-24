# 1. 导入 admin 模块（通常已自动存在于 admin.py）
from django.contrib import admin

# 2. 导入你需要管理的模型（Work）
from .models import Work   # . 表示当前目录（chapters应用内）

# Register your models here.
admin.site.register(Work)