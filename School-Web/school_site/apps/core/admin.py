from django.contrib import admin
from .models import SchoolInfo

# admin.site.site_header = "阳光实验中学 后台管理"      # 登录后顶部标题
# admin.site.site_title = "阳光中学管理"               # 浏览器标签页标题
# admin.site.index_title = "管理面板"      

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # 如果已经有一条记录，则不允许再添加
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)