import turtle
import time


def draw_red_envelope():
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-150, -100)
    turtle.pendown()
    turtle.color('red')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(300)
        turtle.left(90)
        turtle.forward(200)
        turtle.left(90)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-150, -100)
    turtle.pendown()
    turtle.color('gold')
    turtle.pensize(5)
    for _ in range(4):
        turtle.forward(300)
        turtle.left(90)

    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.color('gold')
    turtle.begin_fill()
    turtle.circle(20)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(0, -50)
    turtle.pendown()
    turtle.color('white')
    turtle.write('福', align='center', font=('SimHei', 30, 'bold'))

    turtle.color("red")
    turtle.penup()
    turtle.goto(0, 145)  # 设置文本显示的位置
    turtle.pendown()
    turtle.write("幸福健康！", align="center", font=("Arial", 35, "normal"))
    turtle.penup()
    turtle.goto(0, 100)  # 设置文本显示的位置
    turtle.pendown()
    turtle.write("万事如意！", align="center", font=("Arial", 35, "normal"))

    turtle.hideturtle()
    turtle.done()





turtle.reset()
draw_red_envelope()
draw_wenben1
