#!/usr/bin/env python3

import pygame, random

class Bloco:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.x = x
        self.y = y
        self.color = [random.randint(100,255),random.randint(100,255),random.randint(100,255)]
        self.tela.addblock(self)

    def move(self, x, y):
        if self.tela.getmatrizn(x,y)==1:
            return False
        else:
            self.x = x
            self.y = y
            return True

    def canmove(self, x,y):
        if x<0:
            return False
        if x>10:
            return False
        if y>14:
            return False
        if self.tela.getmatrizn(x,y)==1:
            return False
        else:
            return True
    def x1(self):
        return 25 + self.x*32

    def y1(self):
        return 65 + self.y*32

    def width(self):
        return 30

    def height(self):
        return 30

    def destroyme(self):
        self.tela.destroyblock(self)

    def getcolor(self):
        #aux = self.color
        #self.color = [random.randint(100,255),random.randint(100,255),random.randint(100,255)]
        return self.color

class Peca:
    def __init__(self, tela, n=-1):
        #Ponto central 5
        self.tela = tela
        self.blocos = []
        self.Colidiu = False

        if n==-1:
            n = random.randint(0,5)

        self.n = n

        if self.n == 0:
            #Quadrado
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 6, -1))
            self.blocos.append(Bloco(self.tela, 6, 0))
            self.blocos.append(Bloco(self.tela, 5, 0))
        elif self.n==1:
            #L
            self.blocos.append(Bloco(self.tela, 5, -2))
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))
            self.blocos.append(Bloco(self.tela, 6, 0))
        elif self.n==2:
            #L invertido
            self.blocos.append(Bloco(self.tela, 5, -2))
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))
            self.blocos.append(Bloco(self.tela, 4, 0))
        elif self.n==3:
            #|-
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))
            self.blocos.append(Bloco(self.tela, 4, 0))
            self.blocos.append(Bloco(self.tela, 6, 0))
        elif self.n==4:
            #N1
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 6, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))
            self.blocos.append(Bloco(self.tela, 4, 0))
        elif self.n==5:
            #N2
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 4, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))
            self.blocos.append(Bloco(self.tela, 6, 0))
        elif self.n==6:
            #P
            self.blocos.append(Bloco(self.tela, 5, -3))
            self.blocos.append(Bloco(self.tela, 5, -2))
            self.blocos.append(Bloco(self.tela, 5, -1))
            self.blocos.append(Bloco(self.tela, 5, 0))


    def move(self, direction, steps):
        if direction == "right":
            for bloco in self.blocos:
                if not bloco.canmove(bloco.x+1, bloco.y):
                    return False
            for bloco in self.blocos:
                bloco.move(bloco.x+1, bloco.y)

        if direction == "left":
            for bloco in self.blocos:
                if not bloco.canmove(bloco.x-1, bloco.y):
                    return False
            for bloco in self.blocos:
                bloco.move(bloco.x-1, bloco.y)

        if direction == "down":
            for bloco in self.blocos:
                if not bloco.canmove(bloco.x, bloco.y+1):
                    self.Colidiu = True
                    return False
            for bloco in self.blocos:
                bloco.move(bloco.x, bloco.y+1)

            return True

        if direction == "up":
            for bloco in self.blocos:
                if not bloco.canmove(bloco.x, bloco.y-1):
                    return False
            for bloco in self.blocos:
                bloco.move(bloco.x, bloco.y-1)

    def registrablocos(self):
        for bloco in self.blocos:
            self.tela.matriz[bloco.x][bloco.y]=1


class Telinha:
    def __init__(self, surface, x1, x2, y1, y2):
        self.surface = surface
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.Finished = False
        self.color = 255, 255, 255
        self.repository = []
        self.previous = random.randint(0, 6)
        self.counte = 0

        self.pecaatual = Peca(self, random.randint(0, 5))

        self.matriz = []
        for i in range(0,30):
            self.matriz.append([])
            for j in range (0,16):
                self.matriz[i].append(0)
        print(self.matriz)



    def addblock(self, bloco):
        self.repository.append(bloco)


    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x1, self.y1, self.x2, self.y2), 1)
        for bloco in self.repository:
            if bloco.y>=0:
                pygame.draw.rect(self.surface, bloco.getcolor(), (bloco.x1(), bloco.y1(), bloco.width(),  bloco.height()), 0)



    def drawgame(self):
        pygame.display.set_caption("jubs tetris. => press Esc to quit. FPS: %.2f %.2f" % (clock.get_fps(), clock.get_rawtime()))
        #fontsize = random.randint(35, 150)
        myFont = pygame.font.SysFont('freesansbold.ttf', fontsize)

        color = (0, 0, random.randint(80,150))

        screen.fill(bg)
        screen.blit(myFont.render("myLitteTetris:", 0, (color)), (x,y))
        self.draw()
        if self.anyonfirst():
            self.Finished = True

        self.deletefulllines()


        self.registrablocos()
        self.deleteline(15)

    def getprevious(self):
        n = self.previous
        self.previous = random.randint(0, 6)
        return n

    def moveatualdon(self):
        self.pecaatual.move("down",1)
        if self.pecaatual.Colidiu:
            self.pecaatual.registrablocos()
            self.pecaatual = Peca(self, self.getprevious())

    def action(self, key):
        if key == pygame.K_DOWN:
            self.moveatualdon()
        elif key == pygame.K_LEFT:
            self.pecaatual.move("left",1)
        elif key == pygame.K_RIGHT:
            self.pecaatual.move("right",1)
        elif key == pygame.K_d:
            print(self.matriz)

    def getmatrizn(self, x, y):
        if y<0:
            return 0
        else:
            return self.matriz[x][y]

    def fullcolumn(self, x):
        for y in range (0, 15):
            if self.matriz[x][y]==0:
                return False
        return True

    def fullline(self, y):
        for x in range (0, 11):
            if self.matriz[x][y]==0:
                return False
        return True

    def anyfullcolumn(self):
        for x in range(0, 10):
            if self.fullcolumn(x):
                return True
        return False

    def anyfullline(self):
        for y in range(0, 15):
            if self.fullline(y):
                return True
        return False

    def anyonfirst(self):
        for x in range(0, 11):
            if self.matriz[x][0]==1:
                return True

    def deletefulllines(self):
        for y in range(0, 15):
            if self.fullline(y):
                self.deletelinedown(y)


    def deletelinedown(self, y):
        for bloco in self.repository:
            if bloco.y == y:
                bloco.destroyme()

        self.limpamatriz()
        for bloco in self.repository:
            if bloco not in self.pecaatual.blocos:
                if bloco.y<y:
                    bloco.move(bloco.x, bloco.y+1)
        self.registrablocos

    def deleteline(self, y):
        for bloco in self.repository:
            if bloco.y == y:
                bloco.destroyme()


    def limpamatriz(self):
        for x in range(0,11):
            for y in range(0,15):
                self.matriz[x][y] = 0

    def registrablocos(self):
        for bloco in self.repository:
            if bloco not in self.pecaatual.blocos:
                self.matriz[bloco.x][bloco.y]=1


    def destroyblock(self, bloco):
        print (bloco.x, bloco.y)
        self.repository.remove(bloco)



pygame.init()

bg = [0,0,0]

screen = pygame.display.set_mode([ 500,600])
screen.fill(bg)

mainloop, x,y, color, fontsize, delta, fps =  True, 20, 10, (32,32,32), 35, 1, 30

clock = pygame.time.Clock() # create clock object
telinha = Telinha(screen, 20, 360, 60, 490)

pygame.key.set_repeat(200, 30)

while mainloop:
    tick_time = clock.tick(fps) # milliseconds since last frame

    telinha.drawgame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            telinha.action(event.key)
    if telinha.Finished:
        mainloop = False

    pygame.display.update()
