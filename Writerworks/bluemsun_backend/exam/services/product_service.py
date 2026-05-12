# exam/services/product_service.py
"""
业务逻辑层 - 商品服务（第四题）
"""
from decimal import Decimal
from django.db import transaction
from exam.models import Product

class ProductService:
    """商品相关业务逻辑，包含事务操作"""

    @staticmethod
    def insert_products_with_transaction(products_data):
        """
        事务插入商品，模拟失败场景（插入重复主键会回滚）
        因为Django模型使用自增主键，重复主键需要手动指定id。
        为了演示回滚，尝试插入一条id=1的已存在记录（假设之前有id=1）
        """
        try:
            with transaction.atomic():
                for product in products_data:
                    # 如果存在id字段且为重复主键，会触发IntegrityError
                    Product.objects.create(**product)
                return True, "所有商品插入成功"
        except Exception as e:
            return False, f"插入失败，已回滚：{str(e)}"

    @staticmethod
    def get_expensive_products(price_threshold=50):
        """查询价格大于指定阈值的商品"""
        return Product.objects.filter(price__gt=price_threshold)

    @staticmethod
    def increase_stock_all(increment=10):
        """
        将所有商品的库存增加10，使用事务
        """
        try:
            with transaction.atomic():
                updated = Product.objects.update(stock=models.F('stock') + increment)
                return True, f"成功更新 {updated} 条记录，库存增加 {increment}"
        except Exception as e:
            return False, f"更新失败，已回滚：{str(e)}"