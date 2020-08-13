import pygame
from pygame.locals import *
import random
pygame.init()
width=800
height=600
win=pygame.display.set_mode((width,height))
pygame.display.set_caption('Running Dino')
clock=pygame.time.Clock()
pygame.time.set_timer(USEREVENT+2,4000)
fps=25
floor=[pygame.image.load('2.png')]
bg=pygame.image.load('BG.png')
bg=pygame.transform.scale(bg,(width,height))
font=pygame.font.SysFont(None,50)
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)

foot=520
fy=450
defaultBlockX=fy+15
win.fill((255, 255, 255))
run=True
isRun=False

totalBlock=0
intervalList=[]
quantityList=[]
crator1loc = width+30
passedBlock1=0
floorSurface=fy+70

bgX=0
bgLastX=bg.get_width()


class dino(object):
    running = [pygame.image.load('Run (1).png'), pygame.image.load('Run (2).png'), pygame.image.load('Run (3).png'),
               pygame.image.load('Run (4).png'), pygame.image.load('Run (5).png'), pygame.image.load('Run (6).png'),
               pygame.image.load('Run (7).png'), pygame.image.load('Run (8).png')]
    jumpingup = [pygame.image.load('Jump (1).png'), pygame.image.load('Jump (2).png'),
                 pygame.image.load('Jump (3).png'), pygame.image.load('Jump (4).png'),
                 pygame.image.load('Jump (5).png'), pygame.image.load('Jump (6).png')]
    jumpingdown = [pygame.image.load('Jump (7).png'), pygame.image.load('Jump (8).png'),
                   pygame.image.load('Jump (9).png'), pygame.image.load('Jump (10).png'),
                   pygame.image.load('Jump (11).png'), pygame.image.load('Jump (12).png')]
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.isUp=False
        self.isDown=False
        self.incrementMax=210
        self.increment=30
        self.walk=0
        self.jumpup=1
        self.jumpdown=0
        for n in range(0, 6):
            self.jumpingup[n] = pygame.transform.scale(self.jumpingup[n], (80, 80))
            self.jumpingdown[n] = pygame.transform.scale(self.jumpingdown[n], (80, 80))
        for n in range(0, 8):
            self.running[n] = pygame.transform.scale(self.running[n], (80, 80))
    def updatedino(self,speed,win):
        global bgX,playerdino,image,jmage,jdmage
        self.hitbox = (self.x, self.y+5, 60, 60)
        if self.walk >= len(self.running) - 1:
            self.walk = 0
        image = self.running[self.walk]
        # DisplayLabel = font.render('Passed Blocks: ', 30, black)
        # DisplayValue = font.render(str(totalBlock), 30, black)
        clock.tick(fps)
        if self.isUp:
            if self.isDown:
                jmage = self.jumpingdown[self.jumpdown]
                self.y += self.increment
                self.jumpdown += 1
                if playerdino.jumpdown>=len(self.jumpingdown)-1:
                    playerdino.jumpdown=len(self.jumpingdown)-1
                # win.blit(jmage, (self.x, self.y))
                if playerdino.y == fy:
                    self.isDown=False
                    self.isUp=False
                    self.jumpup, self.jumpdown = 1, 0
            else:
                jmage = self.jumpingup[playerdino.jumpup]
                #if self.jumpup>=2:
                self.y -= playerdino.increment
                # win.blit(jmage, (self.x, self.y))
                playerdino.jumpup += 1
                if self.jumpup >= len(self.jumpingup)-1:
                    self.jumpup = len(self.jumpingup)-1
                if self.y <= fy - self.incrementMax:
                    self.isDown=True
            win.blit(jmage, (self.x, self.y))
        else:
            clock.tick(fps+speed)
            win.blit(image, (self.x, self.y))
            self.walk += 1
        pygame.draw.rect(win,red,self.hitbox,2)
        # win.blit(DisplayLabel,(0,0))
        # win.blit(DisplayValue,(280,0))


def flooring():
    global bg
    bg = bg.copy()
    for i in range(-1, 7):
        bg.blit(floor[0], (playerdino.x + i * 100, floorSurface))

obstacleList=[]
# quantity=random.randint(1,1)
# quantityList.append(quantity)
# obstacleList.append(crator1loc)

class cratorClass(object):
    obstacle = [pygame.image.load('Crate.png')]
    obstaclesize = 55
    def __init__(self,x,y,quantity):
        self.x=x
        self.y=y
        self.quantity=quantity
        self.obstacle[0] = pygame.transform.scale(self.obstacle[0], (self.obstaclesize, self.obstaclesize))
    def drawCrator(self,win):
        self.hitbox=(self.x,self.y,self.obstaclesize,self.obstaclesize)
        pygame.draw.rect(win,red,self.hitbox,1)
        win.blit(self.obstacle[0],(self.x,self.y))
    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False
o=0
def window():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgLastX, 0))
    playerdino.updatedino(0, win)
    for obstacle in obstacleList:
        cratorClass.drawCrator(obstacle,win)
        obstacle.x-=fps

    pygame.display.update()

    # if (((playerdino.x > crator1loc-obstaclesize) and (playerdino.x<crator1loc+obstaclesize))):
    #     if playerdino.y + 70 < floorSurface - obstaclesize * quantityList[passedBlock1]:
    #         pass
    #     else:
    #         pygame.quit()
    # else:
    #     pass
    # if ((playerdino.x > crator2loc-obstaclesize) and (playerdino.x<crator2loc+obstaclesize)):
    #     if playerdino.y + 70 < floorSurface - obstaclesize * quantityList2[passedBlock2]:
    #         pass
    #     else:
    #         pygame.quit()
    # else:
    #     pass

playerdino=dino(100,450)
#image=dino.running[playerdino.walk]
flooring()
while run:
    #win.blit(bg, (0, 0))
    clock.tick(fps/2)
    bgX-=fps
    bgLastX-=fps
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     isRun = True
    #     message('press Space to start running')
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==USEREVENT+2:
            r=random.randint(0,2)
            obstacleList.append(cratorClass(810,defaultBlockX,r))
            quantity = random.randint(0, 2)
            quantityList.append(quantity)
    if keys[pygame.K_UP]:
        playerdino.isUp=True
        # playerdino.updatedino(0, win)
    else:
        pass
        # playerdino.updatedino(0, win)
    window()
    if bgX<=-800:
        bgX=bg.get_width()
    if bgLastX<=-800:
        bgLastX=bg.get_width()
    pygame.display.update()

pygame.quit()

