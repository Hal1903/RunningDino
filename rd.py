import pygame
from pygame.locals import *
import random

pygame.init()
width=800
height=600
win=pygame.display.set_mode((width,height))
pygame.display.set_caption('Running Dino')
clock=pygame.time.Clock()
pygame.time.set_timer(USEREVENT+2,random.randint(2000,2500))
fps=20
floor=[pygame.image.load('2.png')]
bg=pygame.image.load('BG.png')
bg=pygame.transform.scale(bg,(width,height))
font=pygame.font.SysFont(None,50)
white=(255,255,255,1)
black=(0,0,0,1)
red=(255,0,0,1)

foot=520
fy=450
defaultBlockX=fy+15
win.fill(white)
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
bg2=bg.copy()
numEvent=0

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
        self.incrementMax=175
        self.increment=25
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
        self.hitbox = (self.x, self.y, 60, 60)
        if self.walk >= len(self.running) - 1:
            self.walk = 0
        image = self.running[self.walk]
        clock.tick(fps+speed)
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
        #pygame.draw.rect(win,red,self.hitbox,2)

def flooring():
    global bg
    bg = bg.copy()
    for i in range(-1,7):
        bg.blit(floor[0], (playerdino.x + i * 100, floorSurface))

obstacleList=[]
# quantity=random.randint(1,1)
# quantityList.append(quantity)
# obstacleList.append(crator1loc)

class cratorClass(object):
    global floorSurface, numEvent
    obstacle = [pygame.image.load('Crate.png')]
    obstaclesize = 55
    def __init__(self,x,y,quant):
        self.x=x
        self.y=y
        self.quant=quant
        self.obstacle[0] = pygame.transform.scale(self.obstacle[0], (self.obstaclesize, self.obstaclesize))
    def drawCrator(self,win):
        #edit it to regard quantity by multiply y
        self.hitbox=(self.x,self.y,self.obstaclesize,self.obstaclesize)
        win.blit(self.obstacle[0],(self.x,self.y))
        #pygame.draw.rect(win, red, self.hitbox, 2)
        if self.quant==2:
            win.blit(self.obstacle[0],(self.x,self.y-55))
            pygame.draw.rect(win, red, (self.x,self.y-55,self.obstaclesize,self.obstaclesize), 2)
    def collide(self,rect):
        if self.quant==2:
            if ((rect[0]+40>self.hitbox[0]) and (rect[0]<self.hitbox[0]+self.obstaclesize)):
                if rect[1]+60<floorSurface-self.obstaclesize*2-20:
                    return False
                else:
                    return True
            else:
                return False
        if self.quant==1:
            if ((rect[0]+40>self.hitbox[0]) and (rect[0]<self.hitbox[0]+self.obstaclesize)):
                if rect[1]+60<floorSurface-self.obstaclesize-15:
                    return False
                else:
                    return True
            else:
                return False

def countBlock():
    global obstacleList,totalBlock
    DisplayLabel = font.render('Passed Blocks: ', 30, black)
    DisplayValue = font.render(str(totalBlock), 30, black)
    win.blit(DisplayLabel, (0, 0))
    win.blit(DisplayValue, (280, 0))

def scoreDoc():
    f=open('score.txt','r')
    file=f.readlines()
    bestScore=int(file[0])
    if totalBlock>int(bestScore):
        f.close()
        file=open('score.txt','w')
        file.write(str(totalBlock))
        file.close()
        #return totalBlock
    f.close()
    return bestScore

def LastScore():
    f=open('Lscore.txt','r')
    file=f.readlines()
    last=int(file[0])
    f.close()
    return last
def LastUpdate():
    file=open('Lscore.txt','w')
    file.write(str(totalBlock))
    file.close()
    f.close()

def endWindow():
    global totalBlock
    endrun=True
    pygame.time.delay(500)
    while endrun:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                endrun=False
        win.blit(bg2,(0,0))
        DisplayScore=font.render('Your Score:'+str(totalBlock),45,black)
        scoreBest=font.render('Your Best Score:'+str(scoreDoc()),25,black)
        scoreLast=font.render('Your Last Score:'+str(LastScore()),25,black)
        win.blit(DisplayScore,(200,200))
        win.blit(scoreBest, (200, 300))
        win.blit(scoreLast,(200,400))
        pygame.display.update()
    if not endrun:
        LastUpdate()

o=0
spd=0
def window():
    global totalBlock,run
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgLastX, 0))
    playerdino.updatedino(spd, win)
    for obstacle in obstacleList:
        cratorClass.drawCrator(obstacle,win)
        obstacle.x-=fps
        if obstacle.x <= -55:
            totalBlock += 1
            obstacleList.pop(obstacleList.index(obstacle))
        if obstacle.collide(playerdino.hitbox)==True:
            run=False
            endWindow()
    countBlock()
    pygame.display.update()

playerdino=dino(100,450)
#image=dino.running[playerdino.walk]
flooring()

while run:
    #win.blit(bg, (0, 0))
    fps=20
    clock.tick(fps)
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
            numEvent+=1
            quantity = random.randint(1,2)
            quantityList.append(quantity)
            obstacleList.append(cratorClass(840,defaultBlockX,quantityList[numEvent-1]))
            print(quantityList)
    if keys[pygame.K_UP]:
        playerdino.isUp=True
        # playerdino.updatedino(0, win)
    if keys[pygame.K_RIGHT]:
        spd=15
    else:
        spd=0
        # playerdino.updatedino(0, win)
    window()
    if bgX<=-800:
        bgX=bg.get_width()
    if bgLastX<=-800:
        bgLastX=bg.get_width()
    pygame.display.update()

pygame.quit()
