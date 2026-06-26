"""
初始化种子数据：创建 admin / 教师 / 学生 / 课程 / 知识点 / 题目 / 试卷 / 资料
运行方式：python manage.py shell -c "exec(open('seed.py').read())"
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Student, Teacher, Role
from courses.models import Course, KnowledgePoint
from exams.models import Question, Exam, ExamQuestion
from materials.models import Material

User = get_user_model()

print('=== 清理旧数据 ===')
User.objects.filter(username__in=['admin', 'teacher', 'student1']).delete()
Course.objects.all().delete()
Question.objects.all().delete()
Exam.objects.all().delete()
Material.objects.all().delete()

print('=== 创建用户 ===')
admin = User.objects.create_superuser(username='admin', password='admin123', email='admin@test.com', phone='13800000001')
teacher_u = User.objects.create_user(username='teacher', password='teacher123', role=Role.TEACHER, email='teacher@test.com')
teacher = Teacher.objects.create(user=teacher_u, teacher_no='T001', name='李老师', title='副教授', department='计算机学院')
student_u = User.objects.create_user(username='student', password='student123', role=Role.STUDENT, email='student@test.com', phone='13900000001')
student = Student.objects.create(user=student_u, student_no='2025001', name='张同学', college='计算机学院', major='软件工程', grade='2023级', contact='13900000001')

print('=== 创建课程 ===')
course1 = Course.objects.create(code='CS101', name='Python 程序设计', description='Python 入门到精通', teacher=teacher_u)
course2 = Course.objects.create(code='CS201', name='数据结构', description='常用数据结构与算法', teacher=teacher_u)

print('=== 创建知识点 ===')
kp1_root = KnowledgePoint.objects.create(course=course1, parent=None, title='Python 基础', order_no=1)
kp1_1 = KnowledgePoint.objects.create(course=course1, parent=kp1_root, title='变量与数据类型', order_no=1)
kp1_2 = KnowledgePoint.objects.create(course=course1, parent=kp1_root, title='流程控制', order_no=2)
kp1_3 = KnowledgePoint.objects.create(course=course1, parent=kp1_root, title='函数与模块', order_no=3)

kp2_root = KnowledgePoint.objects.create(course=course2, parent=None, title='线性结构', order_no=1)
kp2_1 = KnowledgePoint.objects.create(course=course2, parent=kp2_root, title='数组', order_no=1)
kp2_2 = KnowledgePoint.objects.create(course=course2, parent=kp2_root, title='链表', order_no=2)

print('=== 创建资料 ===')
Material.objects.create(course=course1, kp=kp1_1, title='Python 变量与数据类型讲解', material_type='document',
                         url='https://docs.python.org/zh-cn/3/tutorial/introduction.html', uploader=teacher_u, view_count=10)
Material.objects.create(course=course1, kp=kp1_1, title='类型转换视频', material_type='video',
                         url='https://www.bilibili.com/video/BV1pE411s7bq', duration=600, uploader=teacher_u)
Material.objects.create(course=course1, kp=kp1_2, title='流程控制 if/for/while 文档', material_type='document',
                         url='https://docs.python.org/zh-cn/3/tutorial/controlflow.html', uploader=teacher_u)
Material.objects.create(course=course1, kp=kp1_3, title='函数定义视频', material_type='video',
                         url='https://www.bilibili.com/video/BV1qx411V7qK', duration=900, uploader=teacher_u)
Material.objects.create(course=course2, kp=kp2_1, title='数组基础', material_type='document',
                         description='# 数组\n\n数组是最常用的数据结构之一...', uploader=teacher_u)
Material.objects.create(course=course2, kp=kp2_2, title='链表图解', material_type='link',
                         url='https://visualgo.net/zh/list', uploader=teacher_u)

print('=== 创建题库 ===')
questions = [
    Question(course=course1, kp=kp1_1, question_type='single',
             title='下面哪个是 Python 的整型类型？',
             options={'A': 'int', 'B': 'Integer', 'C': 'number', 'D': 'Int'},
             correct_answer='A',
             analysis='Python 中整型用 int 关键字表示',
             difficulty=1, creator=teacher_u),
    Question(course=course1, kp=kp1_1, question_type='single',
             title='以下代码 x = "123" 中，x 的类型是？',
             options={'A': 'int', 'B': 'str', 'C': 'list', 'D': 'float'},
             correct_answer='B',
             analysis='双引号括起来的是字符串 str',
             difficulty=1, creator=teacher_u),
    Question(course=course1, kp=kp1_2, question_type='judge',
             title='Python 的 for 循环可以遍历列表。',
             options={'A': '正确', 'B': '错误'},
             correct_answer=True,
             analysis='for i in [1,2,3] 是合法写法',
             difficulty=1, creator=teacher_u),
    Question(course=course1, kp=kp1_2, question_type='multi',
             title='以下哪些是 Python 的关键字？',
             options={'A': 'if', 'B': 'for', 'C': 'print', 'D': 'while'},
             correct_answer=['A', 'B', 'D'],
             analysis='print 是内置函数不是关键字',
             difficulty=2, creator=teacher_u),
    Question(course=course1, kp=kp1_3, question_type='single',
             title='定义函数用哪个关键字？',
             options={'A': 'function', 'B': 'def', 'C': 'func', 'D': 'define'},
             correct_answer='B',
             analysis='Python 用 def 定义函数',
             difficulty=1, creator=teacher_u),
    Question(course=course2, kp=kp2_1, question_type='single',
             title='数组的随机访问时间复杂度是？',
             options={'A': 'O(1)', 'B': 'O(n)', 'C': 'O(log n)', 'D': 'O(n²)'},
             correct_answer='A',
             analysis='数组按下标访问是 O(1)',
             difficulty=2, creator=teacher_u),
    Question(course=course2, kp=kp2_2, question_type='multi',
             title='链表相比数组的优势有？',
             options={'A': '随机访问快', 'B': '插入删除方便', 'C': '内存不必连续', 'D': '遍历更快'},
             correct_answer=['B', 'C'],
             analysis='链表插入删除 O(1)，内存不要求连续',
             difficulty=2, creator=teacher_u),
]
for q in questions:
    q.save()

print('=== 创建试卷 ===')
exam1 = Exam.objects.create(course=course1, title='Python 基础小测', description='Python 前 3 个知识点测试',
                              duration_minutes=15, passing_score=60, total_score=100,
                              status=Exam.Status.PUBLISHED, creator=teacher_u)
exam2 = Exam.objects.create(course=course2, title='数据结构小测', description='数组 + 链表测试',
                              duration_minutes=10, passing_score=60, total_score=100,
                              status=Exam.Status.PUBLISHED, creator=teacher_u)

q_list1 = Question.objects.filter(course=course1).order_by('id')
for i, q in enumerate(q_list1):
    ExamQuestion.objects.create(exam=exam1, question=q, score=20, order_no=i+1)
Exam.objects.filter(pk=exam1.pk).update(total_score=100)

q_list2 = Question.objects.filter(course=course2).order_by('id')
for i, q in enumerate(q_list2):
    ExamQuestion.objects.create(exam=exam2, question=q, score=50, order_no=i+1)
Exam.objects.filter(pk=exam2.pk).update(total_score=100)

print('=== 学生成绩 ===')
from accounts.models import StudentCourse
StudentCourse.objects.create(student=student, course=course1, score=85.5, semester='2025-2026-1')
StudentCourse.objects.create(student=student, course=course2, score=90.0, semester='2025-2026-1')

print('=== 种子数据创建完成 ===')
print('账号：')
print('  admin / admin123   (管理员)')
print('  teacher / teacher123 (教师)')
print('  student / student123 (学生)')
print(f'  课程 {Course.objects.count()} 个，知识点 {KnowledgePoint.objects.count()} 个')
print(f'  题目 {Question.objects.count()} 道，试卷 {Exam.objects.count()} 个')
print(f'  资料 {Material.objects.count()} 个')
