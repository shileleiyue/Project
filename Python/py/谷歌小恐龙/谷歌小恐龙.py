
import pygame, sys, os, random, time
from pygame import mixer

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
canvas = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('小恐龙')
xrz = pygame.image.load('images/仙人掌.png')
kl1 = pygame.image.load('images/恐龙1.png')
kl2 = pygame.image.load('images/恐龙2.png')
kl2 = pygame.tranform.scale(kl2, (82, 76))

js = mixer.Soud('souds/跳跃音效.wav')
ls = mixer.Soud('souds/失败音效.wav')

def comPaint():
    canvas.fill((255, 255, 255))
    pygame.draw.line(canvas, (100, 100, 100), (0, 575), (1280, 575), 5)


while True:
    comPaint()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



class XKL():
    def __init__(self):
        self.w = 82
        self.h = 76
        self.x = 100
        self.y = 500
        self.j = False
        self.s = -18
        self.i = 1
    def paint(self):
        if Game.state == 'RUNNING':
            if self.i == 1:
                canvas.blit(kl1, (self.x, self.y))
                self.i = 2
            else:
                canvas.blit(kl2, (self.x, self.y))
                self.i = 1
        else:
            canvas.blit(kl1, (self.x, self.y))
    def jump(self):
        if self.j:
            self.y += self.s
            self.s += 1
            if self.y >= 500:
                self.y = 500
                self.s = -18
                self.j = False

class XRZ():
    def __init__(self):
        self.size = random.randint(50, 100)/100
        self.w = int(69*self.size)
        self.h = int(88*self.size)
        self.x = 1280
        self.y = 472 + 103 - self.h
        self.i = pygame.transform.scale(xrz, (self.w, self.h))
        self.s = 15
    def paint(self):
        canvas.blit(self.i, (self.x, self.y))
    def move(self):
        self.x -= self.s

class Game():
    state = 'READY'
    xkl   = XKL()
    xrzs  = []
    it    = 3
    lt    = 0
    score = 0









