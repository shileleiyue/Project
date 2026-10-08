from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def home(request):
    return HttpResponse('''
    <h2>🎓 个性化网络学习空间 · Django API 后端</h2>
    <ul>
      <li>前端页面：<a href="http://127.0.0.1:8080">http://127.0.0.1:8080</a></li>
      <li>API 文档 Swagger：<a href="/api/docs/">/api/docs/</a></li>
      <li>API 文档 ReDoc：<a href="/api/redoc/">/api/redoc/</a></li>
      <li>管理员后台：<a href="/admin/">/admin/</a></li>
    </ul>
    ''')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # JWT 登录 / 刷新
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 业务模块
    path('api/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('materials.urls')),
    path('api/', include('exams.urls')),
    path('api/', include('analytics.urls')),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# 媒体文件（开发模式）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
