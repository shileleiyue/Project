from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('departments/', views.departments, name='departments'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),
    path('leaders/', views.leaders, name='leaders'),
    path('teachers/', views.teachers, name='teachers'),
]