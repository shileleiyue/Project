"""
URL configuration for school_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 各功能模块路由分发
    path('', include('apps.core.urls')),               # 首页等
    path('pages/', include('apps.pages.urls')),         # 固定单页
    path('organization/', include('apps.organization.urls')),
    path('news/', include('apps.news.urls')),           # 新闻/通知/媒体报道
    path('admissions/', include('apps.admissions.urls')),
    path('graduates/', include('apps.graduates.urls')),
    path('contact/', include('apps.contact.urls')),
    path('gallery/', include('apps.gallery.urls')),
]
# 开发环境下让 Django 托管媒体文件（生产环境请用 Nginx）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)