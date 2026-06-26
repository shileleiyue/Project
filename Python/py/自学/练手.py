import pygame
import time
import random
import turtle

pygame.init()

# 定义颜色
white = (255, 255, 255)#白色
black = (0, 0, 0)#黑色
red = (255, 0, 0)#红色
green = (0, 255, 0)#绿色
blue = (0, 0, 255)#蓝色
yellow = (255, 255, 102)#黄色


window = turtle.Screen()
window.title("推箱子游戏")
window.bgcolor("black")
window.setup(500, 500)
window.tracer(0)  # 关闭动画效果，加快运行速度
time_sleep(4,window)
