
import pygame
import random
pygame.init()
width=800
height=600
win=pygame.display.set_mode((width,height))
pygame.display.set_caption('Running Dino')
clock=pygame.time.Clock()
fps=28
floor=[pygame.image.load('2.png')]
obstacle=[pygame.image.load('Crate.png')]
running=[pygame.image.load('Run (1).png'),pygame.image.load('Run (2).png'),pygame.image.load('Run (3).png'),pygame.image.load('Run (4).png'),pygame.image.load('Run (5).png'),pygame.image.load('Run (6).png'),pygame.image.load('Run (7).png'),pygame.image.load('Run (8).png')]
jumpingup=[pygame.image.load('Jump (1).png'),pygame.image.load('Jump (2).png'),pygame.image.load('Jump (3).png'),pygame.image.load('Jump (4).png'),pygame.image.load('Jump (5).png'),pygame.image.load('Jump (6).png')]
jumpingdown=[pygame.image.load('Jump (7).png'),pygame.image.load('Jump (8).png'),pygame.image.load('Jump (9).png'),pygame.image.load('Jump (10).png'),pygame.image.load('Jump (11).png'),pygame.image.load('Jump (12).png')]
passedBlock1=0
passedBlock2=0
bg=pygame.image.load('BG.png')
bg=pygame.transform.scale(bg,(width,height))
obstaclesize=55
obstacle[0]=pygame.transform.scale(obstacle[0],(obstaclesize,obstaclesize))
merged=bg.copy()
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
quantityList2=[]
crator1loc = width
crator2loc = width
passedBlock1=0
passedBlock2=0
floorSurface=fy+70

for n in range(0,6):
    jumpingup[n] = pygame.transform.scale(jumpingup[n], (80, 80))
    jumpingdown[n] = pygame.transform.scale(jumpingdown[n], (80, 80))
for n in range(0,8):
    running[n] = pygame.transform.scale(running[n], (80,80))
class dino(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.isUp=False
        self.isDown=False
        self.incrementMax=160
        self.increment=20
        self.walk=0
        self.jumpup=1
        self.jumpdown=0
    def updatedino(self,speed,win):
        global playerdino,image,jmage,jdmage,DisplayLabel,DisplayValue
        if playerdino.walk >= len(running) - 1:
            playerdino.walk = 0
        image = running[playerdino.walk]
        DisplayLabel = font.render('Passed Blocks: ', 30, white)
        DisplayValue = font.render(str(totalBlock), 30, white)
        clock.tick(fps)
        if playerdino.isUp:
            clock.tick(fps)
            flooring()
            if playerdino.isDown:
                win.blit(floor[0], (playerdino.x, playerdino.y + 70))
                jmage = jumpingdown[playerdino.jumpdown]
                playerdino.y += playerdino.increment
                flooring()
                drawcrators(playerdino.increment)

                win.blit(jmage, (playerdino.x, playerdino.y))
                playerdino.jumpdown += 1
                if playerdino.jumpdown>=len(jumpingdown)-1:
                    playerdino.jumpdown=len(jumpingdown)-1
                if playerdino.y == fy:
                    playerdino.isDown=False
                    playerdino.isUp=False
                    playerdino.jumpup, playerdino.jumpdown = 1, 0
            else:
                jmage = jumpingup[playerdino.jumpup]
                if playerdino.jumpup>=2:
                    playerdino.y -= playerdino.increment
                win.blit(merged, (0,0))
            #         flooring()
                drawcrators(playerdino.increment)

                win.blit(jmage, (playerdino.x, playerdino.y))
                playerdino.jumpup += 1
                if playerdino.jumpup >= len(jumpingup)-1:
                    playerdino.jumpup = len(jumpingup)-1

                if playerdino.y <= fy - playerdino.incrementMax:
                    playerdino.isDown=True
        else:
            clock.tick(fps+speed)
            flooring()
            drawcrators(playerdino.increment)
            win.blit(image, (playerdino.x, playerdino.y))
            playerdino.walk += 1
        win.blit(DisplayLabel,(0,0))
        win.blit(DisplayValue,(280,0))
        pygame.display.update()

def flooring():
    global merged
    merged = bg.copy()
    for i in range(-1, 7):
        merged.blit(floor[0], (playerdino.x + i * 100, floorSurface))
    win.blit(merged, (0, 0))

def drawcrators(speed):
    global playerdino,x,totalBlock,crator1loc,crator2loc,passedBlock1,passedBlock2,quantityList,defaultBlockX
    interval = random.randrange(100, 200, 10)
    intervalList.append(interval)
    crator2loc = width + intervalList[len(intervalList)-1]
    a=0
    quantity=random.randint(1,2)
    quantityList.append(quantity)
    quantity2 = random.randint(3, 5)
    quantityList2.append(quantity2)
    crator1loc -= fps/2
    crator2loc -= fps/2
    if crator1loc<-60:
        crator1loc=width
        passedBlock1+=1
    for x in range(0,quantityList[passedBlock1]):
        merged.blit(obstacle[0], (crator1loc, defaultBlockX-a))
        a += 55
    totalBlock=passedBlock1+passedBlock2
    
    pygame.draw.line(merged, black, (0, floorSurface-55), (width, floorSurface-55), 1)
    pygame.draw.line(merged, red, (0, playerdino.y + 70), (width, playerdino.y + 70), 1)
    pygame.draw.line(merged, white, (0, playerdino.y), (width, playerdino.y), 1)

    win.blit(merged,(0,0))
    if ((playerdino.x+55 > crator1loc) and (playerdino.x>crator1loc+40)):
        if playerdino.y+70<floorSurface-55:
            print('over the block')
        else:
            pygame.quit()
    else:
        pass

playerdino=dino(100,450)
image=running[playerdino.walk]

while run:
    #win.blit(bg, (0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        isRun = True
        message('press Space to start running')
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if keys[pygame.K_UP]:
        playerdino.isUp=True
        dino.updatedino(playerdino, 0, win)
    if keys[pygame.K_RIGHT]:
        dino.updatedino(playerdino, 6, win)
    elif keys[pygame.K_LEFT]:
        dino.updatedino(playerdino, -6, win)
    else:
        dino.updatedino(playerdino, 0, win)
    dino.updatedino(playerdino, 0, win)
    pygame.display.update()

pygame.quit()

