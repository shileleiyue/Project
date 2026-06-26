from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:message_id>/star/', views.toggle_star, name='toggle_star'),
    path('messages/<int:message_id>/tag/<int:tag_id>/', views.tag_message, name='tag_message'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/archive/', views.toggle_archive, name='toggle_archive'),
]