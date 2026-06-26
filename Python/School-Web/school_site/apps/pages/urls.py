from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.page_detail, {'page_type': 'about'}, name='about'),
    path('school_history/', views.page_detail, {'page_type': 'school_history'}, name='school_history'),
    path('campus_culture/', views.page_detail, {'page_type': 'campus_culture'}, name='campus_culture'),
    path('education_philosophy/', views.page_detail, {'page_type': 'education_philosophy'}, name='education_philosophy'),
    path('school_vision/', views.page_detail, {'page_type': 'school_vision'}, name='school_vision'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]