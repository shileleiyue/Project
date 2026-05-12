# exam/views.py
"""
网络层 - 视图处理HTTP请求
"""
import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models as db_models


from exam.services.user_service import UserService
from exam.services.book_service import BookService
from exam.services.product_service import ProductService
from exam.models import Product, Book, User

# ---------- 辅助函数：登录状态检查 ----------
def check_login(request):
    """检查session中是否保持登录状态"""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return UserService.get_user_by_id(user_id)

# ---------- 页面入口 ----------
def index(request):
    """渲染主页面"""
    return render(request, 'index.html')

# ---------- 第五题：登录接口 ----------
@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    """
    用户登录接口
    参数JSON: {"username": "admin", "password": "admin"}
    返回JSON: {"code": 200, "msg": "success"} 或 {"code": 500, "msg": "error"}
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({"code": 500, "msg": "用户名和密码不能为空"})
        
        user = UserService.authenticate(username, password)
        if user:
            # 保持登录状态：写入session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session.save()
            return JsonResponse({"code": 200, "msg": "success"})
        else:
            return JsonResponse({"code": 500, "msg": "用户名或密码错误"})
    except json.JSONDecodeError:
        return JsonResponse({"code": 500, "msg": "无效的JSON格式"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": f"服务器错误: {str(e)}"})

# ---------- 第六题：检索书籍接口 ----------
@require_http_methods(["GET"])
def book_search(request):
    """
    书籍检索接口
    参数Parameter: id
    返回JSON: {"code": 0, "msg": "检索成功", "data": {...}}
    """
    # 可选：检查登录状态（保持登录状态进阶功能）
    user = check_login(request)
    if not user:
        return JsonResponse({"code": 401, "msg": "未登录，请先登录"})
    
    book_id = request.GET.get('id')
    if not book_id:
        return JsonResponse({"code": 1, "msg": "缺少参数id"})
    
    book = BookService.get_book_by_id(book_id)
    if book:
        return JsonResponse({
            "code": 0,
            "msg": "检索成功",
            "data": {
                "id": book.id,
                "name": book.name,
                "author": book.author
            }
        })
    else:
        return JsonResponse({"code": 1, "msg": "书籍不存在"})

# ---------- 第一题：Book类和EBook类演示 ----------
from exam.utils.book_classes import Book, EBook  # 独立实体类

@require_http_methods(["GET"])
def demo_book_class(request):
    """演示第一题的类和折扣计算"""
    ebook = EBook("Python入门", "张三", 59.9, 2.5)
    discounted_price = ebook.discount(20)  # 20%折扣
    return JsonResponse({
        "code": 0,
        "msg": "第一题演示",
        "book_info": str(ebook),
        "discounted_price": discounted_price,
        "original_price": ebook.price
    })

# ---------- 第二题：文件处理 ----------
@csrf_exempt
@require_http_methods(["POST"])
def process_students_file(request):
    """
    读取students.txt，计算平均分，写入summary.txt
    假设students.txt位于项目根目录
    """
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'students.txt')
        if not os.path.exists(file_path):
            return JsonResponse({"code": 1, "msg": "students.txt文件不存在"})
        
        students = []
        total_score = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 3:
                    name, age_str, score_str = parts
                    age = int(age_str)
                    score = int(score_str)
                    student = {"name": name, "age": age, "score": score}
                    students.append(student)
                    total_score += score
        
        if not students:
            return JsonResponse({"code": 1, "msg": "文件中无有效数据"})
        
        avg_score = total_score / len(students)
        
        # 写入summary.txt
        summary_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'summary.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"平均分: {avg_score:.2f}\n")
            f.write("学生信息:\n")
            for s in students:
                f.write(f"姓名: {s['name']}, 年龄: {s['age']}, 分数: {s['score']}\n")
        
        return JsonResponse({
            "code": 0,
            "msg": "处理成功",
            "average_score": round(avg_score, 2),
            "student_count": len(students),
            "summary_file": "summary.txt已生成"
        })
    except Exception as e:
        return JsonResponse({"code": 1, "msg": f"处理出错: {str(e)}"})

# ---------- 第四题：数据库事务操作 ----------
@csrf_exempt
@require_http_methods(["POST"])
def demo_transaction_insert(request):
    """
    演示事务插入：插入3条商品记录，模拟失败场景（重复主键导致回滚）
    注意：需要预先存在id=1的商品来模拟冲突
    """
    # 先确保products表中有id=1的记录用于模拟冲突
    Product.objects.get_or_create(id=1, defaults={'name': '测试商品', 'price': 10, 'stock': 100})
    
    products_data = [
        {"id": 2, "name": "商品A", "price": 30.00, "stock": 50},
        {"id": 3, "name": "商品B", "price": 45.00, "stock": 30},
        {"id": 4, "name": "商品C", "price": 60.00, "stock": 20},
        {"id": 1, "name": "重复商品", "price": 99.99, "stock": 10}  # 故意重复主键id=1，导致失败回滚
    ]
    
    success, msg = ProductService.insert_products_with_transaction(products_data)
    if success:
        return JsonResponse({"code": 0, "msg": msg})
    else:
        return JsonResponse({"code": 1, "msg": msg})

@require_http_methods(["GET"])
def query_expensive_products(request):
    """查询价格 > 50 的商品"""
    products = ProductService.get_expensive_products(50)
    data = [{"id": p.id, "name": p.name, "price": float(p.price), "stock": p.stock} for p in products]
    return JsonResponse({"code": 0, "count": len(data), "products": data})

@csrf_exempt
@require_http_methods(["POST"])
def update_stock_all(request):
    """将所有商品的库存增加10，使用事务"""
    success, msg = ProductService.increase_stock_all(10)
    if success:
        return JsonResponse({"code": 0, "msg": msg})
    else:
        return JsonResponse({"code": 1, "msg": msg})

# ---------- 初始化测试数据 ----------
def init_test_data():
    """初始化测试用户和书籍"""
    # 创建测试用户 admin/admin
    User.objects.get_or_create(username='admin', defaults={'password': 'admin'})
    User.objects.get_or_create(username='test', defaults={'password': '123456'})
    
    # 创建测试书籍
    Book.objects.get_or_create(id=1, defaults={'name': '重生之这一次我一定要加入蓝旭', 'author': 'bluemsun'})
    Book.objects.get_or_create(id=2, defaults={'name': 'Django实战', 'author': '张三'})
    Book.objects.get_or_create(id=3, defaults={'name': 'Python高级编程', 'author': '李四'})
    
    # 创建测试商品（用于第四题价格>50查询）
    Product.objects.get_or_create(id=1, defaults={'name': '高端笔记本', 'price': 5999.00, 'stock': 10})
    Product.objects.get_or_create(id=2, defaults={'name': '无线鼠标', 'price': 45.00, 'stock': 100})
    Product.objects.get_or_create(id=3, defaults={'name': '机械键盘', 'price': 299.00, 'stock': 30})
    Product.objects.get_or_create(id=4, defaults={'name': '显示器', 'price': 1299.00, 'stock': 5})