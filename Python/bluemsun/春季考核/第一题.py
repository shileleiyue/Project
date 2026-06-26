# 第一题：定义 Book 类和 EBook 类

class Book:
    """普通书籍类"""
    def __init__(self, title: str, author: str, price: float):
        self.title = title          # 书名
        self.author = author        # 作者
        self.price = price          # 原价

    def discount(self, percent: float) -> float:
        """
        根据折扣百分比计算折后价格
        :param percent: 折扣百分比，如 20 表示打八折（即原价 * (100-20)/100）
        :return: 折后价格
        """
        if not 0 <= percent <= 100:
            raise ValueError("折扣百分比必须在0~100之间")
        return self.price * (100 - percent) / 100

    def __str__(self) -> str:
        """返回书籍基本信息"""
        return f"《{self.title}》 作者：{self.author} 原价：{self.price:.2f}元"


class EBook(Book):
    """电子书类，继承自 Book"""
    def __init__(self, title: str, author: str, price: float, file_size: float):
        super().__init__(title, author, price)   # 调用父类初始化
        self.file_size = file_size               # 文件大小（MB）

    def __str__(self) -> str:
        """重写 __str__，额外显示文件大小"""
        base_info = super().__str__()
        return f"{base_info} 文件大小：{self.file_size} MB"


# 实例化一本电子书并测试
if __name__ == "__main__":
    ebook = EBook("Python从入门到实践", "Eric Matthes", 79.90, 12.5)
    print(ebook)                     # 打印书籍信息
    discount_price = ebook.discount(20)   # 打8折
    print(f"折后价格：{discount_price:.2f}元")