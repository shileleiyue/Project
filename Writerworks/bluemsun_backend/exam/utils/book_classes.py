# exam/utils/book_classes.py
"""
第一题：独立的实体类（Book和EBook）
"""
class Book:
    """书籍类"""
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
    
    def discount(self, percent):
        """根据折扣百分比计算折后价格"""
        if percent < 0 or percent > 100:
            raise ValueError("折扣百分比应在0-100之间")
        return self.price * (1 - percent / 100)
    
    def __str__(self):
        return f"《{self.title}》 作者：{self.author} 价格：¥{self.price:.2f}"

class EBook(Book):
    """电子书类，继承Book"""
    def __init__(self, title, author, price, file_size):
        super().__init__(title, author, price)
        self.file_size = file_size  # 单位MB
    
    def __str__(self):
        return f"{super().__str__()} 文件大小：{self.file_size}MB"