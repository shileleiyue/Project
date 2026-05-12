from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('messages/', views.message_list, name='message_list'),
    path('mailbox/', views.principal_mail, name='principal_mail'),
    path('mail_success/', views.mail_success, name='mail_success'),
]