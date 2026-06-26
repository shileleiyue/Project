from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet, MaterialViewHistoryViewSet

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='materials')
router.register(r'my-learning', MaterialViewHistoryViewSet, basename='my-learning')

urlpatterns = router.urls
