from django.urls import path
from . import views

app_name = 'wechat_bridge'

urlpatterns = [
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/create/', views.account_create, name='account_create'),
    path('accounts/<int:account_id>/edit/', views.account_edit, name='account_edit'),
    path('accounts/<int:account_id>/delete/', views.account_delete, name='account_delete'),
    path('accounts/<int:account_id>/test/', views.test_connection, name='test_connection'),
    path('accounts/<int:account_id>/sync/', views.sync_contacts, name='sync_contacts'),
    path('accounts/<int:account_id>/logs/', views.sync_logs, name='sync_logs'),
    path('accounts/<int:account_id>/login/', views.personal_login, name='personal_login'),
    path('accounts/<int:account_id>/login/status/', views.personal_login_status, name='personal_login_status'),
    path('accounts/<int:account_id>/logout/', views.personal_logout, name='personal_logout'),
    path('send/', views.send_message, name='send_message'),
]