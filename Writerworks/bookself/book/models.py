from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100,verbose_name='书名')
    author = models.CharField(max_length=100,verbose_name='作者')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='价格')

    def __str__(self):
        return self.name



