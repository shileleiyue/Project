from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ExamViewSet, ExamRecordViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'exams', ExamViewSet, basename='exams')
router.register(r'exam-records', ExamRecordViewSet, basename='exam-records')

urlpatterns = router.urls
