from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('albums/', views.album_list, name='album_list'),
    path('albums/<slug:slug>/', views.album_detail, name='album_detail'),
    path('videos/', views.video_list, name='video_list'),
]