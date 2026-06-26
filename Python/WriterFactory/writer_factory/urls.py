"""
URL configuration for writer_factory project.

作家工厂（Writer Factory）—— 本地桌面创作管理应用
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

from core.views import (
    work_list, work_detail, chapter_read, chapter_save, work_delete,
    chapter_delete, trash_view, work_restore, chapter_restore,
    work_hard_delete, chapter_hard_delete, work_rename, chapter_rename,
    work_create, outline_add_root, outline_add_child, outline_view,
)
from core.views import outline_rename, outline_delete, about
from core.views import (
    character_list, character_add, character_edit, character_delete,
)
from core.views import (
    relationship_list, relationship_add, relationship_edit, relationship_delete,
)
from core.views import (
    timeline_list, timeline_add, timeline_edit, timeline_delete,
)
from core.views import tech_tree, tech_add, tech_edit, tech_delete
from core.views import login_view, register_view, logout_view
from core.views import stats_view, stats_update_goal, search_view
from core.views import export_work_txt, export_work_json
from core.views import (
    app_settings_view, app_settings_password, app_settings_storage,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', work_list, name='work_list'),
    path('work/<int:work_id>/', work_detail, name='work_detail'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/', chapter_read, name='chapter_read'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/save/', chapter_save, name='chapter_save'),
    path('work/<int:work_id>/delete/', work_delete, name='work_delete'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/delete/', chapter_delete, name='chapter_delete'),
    path('trash/', trash_view, name='trash'),
    path('work/<int:work_id>/restore/', work_restore, name='work_restore'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/restore/', chapter_restore, name='chapter_restore'),
    path('work/<int:work_id>/hard_delete/', work_hard_delete, name='work_hard_delete'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/hard_delete/', chapter_hard_delete, name='chapter_hard_delete'),
    path('work/<int:work_id>/rename/', work_rename, name='work_rename'),
    path('work/<int:work_id>/chapter/<int:chapter_id>/rename/', chapter_rename, name='chapter_rename'),
    path('work/<int:work_id>/outline/', outline_view, name='outline'),
    path('work/create/', work_create, name='work_create'),
    path('work/<int:work_id>/outline/add_root/', outline_add_root, name='outline_add_root'),
    path('work/<int:work_id>/outline/<int:node_id>/add_child/', outline_add_child, name='outline_add_child'),
    path('work/<int:work_id>/outline/<int:node_id>/rename/', outline_rename, name='outline_rename'),
    path('work/<int:work_id>/outline/<int:node_id>/delete/', outline_delete, name='outline_delete'),
    path('work/<int:work_id>/export/txt/', export_work_txt, name='export_work_txt'),
    path('work/<int:work_id>/export/json/', export_work_json, name='export_work_json'),
    path('about/', about, name='about'),
    path('stats/', stats_view, name='stats'),
    path('stats/update_goal/', stats_update_goal, name='stats_update_goal'),
    path('search/', search_view, name='search'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # 应用设置
    path('settings/', app_settings_view, name='app_settings'),
    path('settings/password/', app_settings_password, name='app_settings_password'),
    path('settings/storage/', app_settings_storage, name='app_settings_storage'),

    # 角色管理
    path('work/<int:work_id>/characters/', character_list, name='character_list'),
    path('work/<int:work_id>/characters/add/', character_add, name='character_add'),
    path('work/<int:work_id>/characters/<int:char_id>/edit/', character_edit, name='character_edit'),
    path('work/<int:work_id>/characters/<int:char_id>/delete/', character_delete, name='character_delete'),

    # 关系管理
    path('work/<int:work_id>/relationships/', relationship_list, name='relationship_list'),
    path('work/<int:work_id>/relationships/add/', relationship_add, name='relationship_add'),
    path('work/<int:work_id>/relationships/<int:rel_id>/edit/', relationship_edit, name='relationship_edit'),
    path('work/<int:work_id>/relationships/<int:rel_id>/delete/', relationship_delete, name='relationship_delete'),

    # 时间线管理
    path('work/<int:work_id>/timeline/', timeline_list, name='timeline_list'),
    path('work/<int:work_id>/timeline/add/', timeline_add, name='timeline_add'),
    path('work/<int:work_id>/timeline/<int:event_id>/edit/', timeline_edit, name='timeline_edit'),
    path('work/<int:work_id>/timeline/<int:event_id>/delete/', timeline_delete, name='timeline_delete'),

    # 科技树管理
    path('work/<int:work_id>/tech_tree/', tech_tree, name='tech_tree'),
    path('work/<int:work_id>/tech_tree/add/', tech_add, name='tech_add'),
    path('work/<int:work_id>/tech_tree/<int:node_id>/edit/', tech_edit, name='tech_edit'),
    path('work/<int:work_id>/tech_tree/<int:node_id>/delete/', tech_delete, name='tech_delete'),
]

# 开发模式下由 Django 静态文件服务处理媒体文件；
# 打包模式（frozen, DEBUG=False）下同样显式挂载 media 与 static，
# 保证 exe 运行时封面图、收集后的静态资源可被访问。
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve,
                {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', static_serve,
                {'document_root': settings.STATIC_ROOT}),
    ]
