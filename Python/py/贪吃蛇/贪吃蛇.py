# 导入pygame
import pygame
import random
import time


# pip3 install

# 初始化pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 102)
green = (0,255,0)
# 初始化变量
dis_width = 800
dis_height = 600

snake_speed = 10
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 25)
scr_font = pygame.font.SysFont("cosmeticians", 35)
s_size = 10

# 设置展示模式
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('贪吃蛇')


def score(scr):
    value = scr_font.render("Your Score: " + str(scr), True, red)
    dis.blit(value, [0, 0])


# 信息函数
def message(msg, color):
    m = font_style.render(msg, True, color)
    dis.blit(m, [dis_width / 3, dis_height / 3])


def draw_snake(snake, size):
    for n in snake:
        pygame.draw.rect(dis, green, [n[0], n[1], size, size])  # rect(display, color, [x, y, width, height])


# 主游戏过程
def game():
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    game_over = False
    game_close = False
    foodx = round(random.randrange(0, dis_width - s_size) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - s_size) / 10.0) * 10.0
    s_len = 1
    s_list = []

    while not game_over:
        while game_close:
            dis.fill(white)
            message("You lose, Press C to play again, Press Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game()

        # 判断事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -s_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = s_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -s_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = s_size
                    x1_change = 0
        # 判断碰到边缘
        if x1 >= dis_width + 1 or x1 <= -1 or y1 >= dis_height+1 or y1 <= -1:
            game_close = True
        # 改变小蛇状态
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, blue, [foodx, foody, s_size, s_size])  # 放上食物

        head = [x1, y1]
        s_list.append(head)
        if len(s_list) > s_len:
            del s_list[0]

        for x in s_list[:-1]:
            if x == head:
                game_close = True

        draw_snake(s_list, s_size)
        score(s_len - 1)
        pygame.display.update()

        # 判断吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - s_size) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - s_size) / 10.0) * 10.0
            s_len += 1

        clock.tick(snake_speed)
    pygame.quit()
    quit()


game()