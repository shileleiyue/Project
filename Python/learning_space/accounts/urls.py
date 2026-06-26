from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, StudentViewSet, TeacherViewSet, StudentCourseViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'student-courses', StudentCourseViewSet, basename='student-courses')

urlpatterns = router.urls
