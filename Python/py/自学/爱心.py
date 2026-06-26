import turtle
import time
import random

def draw_heart(x,y):
    turtle.pensize(10)
    color = random.choice(['red', 'pink'])  # 随机选择颜色
    turtle.color(color)
    turtle.penup()  # 抬起画笔
    turtle.goto(x, y)  # 移动到指定位置
    turtle.pendown()  # 放下画笔
    turtle.begin_fill()
    turtle.left(140)
    turtle.forward(180)
    turtle.circle(-90, 200)
    turtle.setheading(60)
    turtle.circle(-90, 200)
    turtle.forward(180)
    turtle.end_fill()

def draw_wenben1(x, y):
    turtle.color("red")
    turtle.penup()
    turtle.goto(0, -100)  # 设置文本显示的位置
    turtle.pendown()
    turtle.write("我喜欢你，你喜欢我吗", align="center", font=("楷体", 25, "normal"))  # 显示文本

def draw_wenben2(x, y):
    turtle.color("red")
    turtle.penup()
    turtle.goto(0, -100)  # 设置文本显示的位置
    turtle.pendown()
    turtle.write("马娟同学", align="center", font=("楷体", 30, "normal"))  # 显示文本


while True:
    turtle.reset()
    draw_wenben1(0,-45)
    draw_heart(0,-50)
    time.sleep(1)  # 加快跳动速
    turtle.reset()
    draw_wenben2(0,-45 )
    draw_heart(0,-50)
    time.sleep(1)