# exam/services/book_service.py
"""
业务逻辑层 - 书籍服务
"""
from exam.models import Book

class BookService:
    """书籍相关业务逻辑"""

    @staticmethod
    def get_book_by_id(book_id):
        """根据ID获取书籍"""
        try:
            # 确保book_id是整数
            book_id = int(book_id)
            return Book.objects.get(id=book_id)
        except (Book.DoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def get_all_books():
        """获取所有书籍（用于初始化展示）"""
        return Book.objects.all()