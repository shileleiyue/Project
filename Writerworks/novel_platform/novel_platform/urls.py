"""
URL configuration for novel_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chapters.views import work_list,work_detail,chapter_read,chapter_save,work_delete,chapter_delete,trash_view,work_restore,chapter_restore,work_hard_delete,chapter_hard_delete,work_rename,chapter_rename,work_create,outline_add_root,outline_add_child,outline_view
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
    path('work/<int:work_id>/outline/', outline_view, name='outline_view'),
    path('work/create/', work_create, name='work_create'),
    path('work/<int:work_id>/outline/add_root/', outline_add_root, name='outline_add_root'),
    path('work/<int:work_id>/outline/<int:node_id>/add_child/', outline_add_child, name='outline_add_child'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)