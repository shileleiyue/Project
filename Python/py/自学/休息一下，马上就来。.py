import turtle
import time

def draw_wenben1(x, y):
    turtle.color("red")
    turtle.penup()
    turtle.goto(0, -30)  # 设置文本显示的位置
    turtle.pendown()
    turtle.write("稍等一下，马上就来。", align="center", font=("楷体", 40, "normal"))  # 显示文本

while True:
    turtle.reset()
    draw_wenben1(0,-45)
    time.sleep(3)