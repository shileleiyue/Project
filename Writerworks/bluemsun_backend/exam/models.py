# exam/models.py
from django.db import models

class User(models.Model):
    """用户实体类"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # 明文存储（考核简化）
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

class Book(models.Model):
    """书籍实体类"""
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name

class Product(models.Model):
    """商品实体类（第四题）"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name