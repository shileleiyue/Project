import turtle
import time


# 绘制心脏
def draw_heart():
    turtle.pensize(4)
    turtle.color('red')
    turtle.begin_fill()
    turtle.left(140)
    turtle.forward(180)
    turtle.circle(-90, 200)
    turtle.setheading(60)
    turtle.circle(-90, 200)
    turtle.forward(180)
    turtle.end_fill()


# 控制跳动
def heartbeat():
    while True:
        turtle.clear()
        draw_heart()
        turtle.update()
        time.sleep(0.5)
        turtle.clear()
        turtle.pensize(4)
        turtle.color('lightcoral')
        turtle.begin_fill()
        turtle.left(140)
        turtle.forward(180)
        turtle.circle(-90, 200)
        turtle.setheading(60)
        turtle.circle(-90, 200)
        turtle.forward(180)
        turtle.end_fill()
        turtle.update()
        time.sleep(0.5)

import turtle
import time


# 绘制心脏
def draw_heart():
    turtle.pensize(4)
    turtle.color('red')
    turtle.begin_fill()
    turtle.left(140)
    turtle.forward(180)
    turtle.circle(-90, 200)
    turtle.setheading(60)
    turtle.circle(-90, 200)
    turtle.forward(180)
    turtle.end_fill()


# 控制跳动
def heartbeat():
    while True:
        turtle.clear()
        draw_heart()
        turtle.update()
        time.sleep(0.5)
        turtle.clear()
        turtle.pensize(4)
        turtle.color('lightcoral')
        turtle.begin_fill()
        turtle.left(140)
        turtle.forward(180)
        turtle.circle(-90, 200)
        turtle.setheading(60)
        turtle.circle(-90, 200)
        turtle.forward(180)
        turtle.end_fill()
        turtle.update()
        time.sleep(0.5)


# 初始化turtle
turtle.speed(0)
turtle.hideturtle()
turtle.tracer(0)
heartbeat()
# 初始化turtle
turtle.speed(0)
turtle.hideturtle()
turtle.tracer(0)
heartbeat()