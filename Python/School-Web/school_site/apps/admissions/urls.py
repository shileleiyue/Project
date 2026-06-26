from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('brochures/', views.brochures, name='brochures'),
    path('jobs/', views.jobs, name='jobs'),
    path('zhongkao/', views.zhongkao_faq, name='zhongkao_faq'),
]