from django.contrib import admin
from django.urls import path, include
from core.views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('core.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('wechat/', include('wechat_bridge.urls')),
]