# exam/urls.py
from django.urls import path
from exam import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/login', views.user_login, name='user_login'),
    path('book/search', views.book_search, name='book_search'),
    path('demo/book_class', views.demo_book_class, name='demo_book_class'),
    path('demo/process_students', views.process_students_file, name='process_students'),
    path('demo/transaction_insert', views.demo_transaction_insert, name='transaction_insert'),
    path('demo/expensive_products', views.query_expensive_products, name='expensive_products'),
    path('demo/update_stock', views.update_stock_all, name='update_stock'),
]