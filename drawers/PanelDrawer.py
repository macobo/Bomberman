# -*- coding: utf-8 -*-

import pygame, sys
sys.path.append(".")
from misc import *
from drawers.Face import Face
from Fade import fade

class PanelDrawer(object):
    def __init__(self, panelSize, boardSize):
        self.panelSize = panelSize
        self.boardSize = boardSize
        self.getScreen()
        self.font = pygame.font.Font(fontPath, 40)
        self.smallfont = pygame.font.Font(fontPath, 20)
        
    def createFaces(self, map):
        self.writeNames()
        self.h = self.font.size("U")[1]
        self.urmas = Face(URMASPICS, (0,self.h,
                                      self.panelSize,self.panelSize), 
                           map.players[0])
        self.katrin = Face(KATRINPICS, (self.panelSize+self.boardSize,self.h,
                                        self.panelSize,self.panelSize), 
                           map.players[1])
        self.katrin.update()
        self.faces = [(self.urmas, (0, 0)),
                      (self.katrin, (self.panelSize+self.boardSize, 0))]
        self.h += self.katrin.image.get_height()
        
    def writeNames(self):
        self.writeCentered("Urmas", (self.panelSize//2, 0), self.font)
        self.writeCentered("Katrin", (3*self.panelSize//2+self.boardSize, 0), self.font)
        
    def getScreen(self):
        if not hasattr(self, "screen"):
            self.screen = pygame.display.set_mode((self.boardSize+2*self.panelSize, 
                                                   self.boardSize))
        return self.screen
        
    def update(self, flip=True):
        surface = pygame.Surface((self.panelSize, self.boardSize - self.h))
        for face, (x,y) in self.faces:
            face.update()
            self.getScreen().blit(face.image, face.rect)
            self.getScreen().blit(surface, (x,y+self.h))
            write = lambda s,i: self.writeCentered(s, (x+self.panelSize//2, y+self.h+10+30*i), self.smallfont)
            status = face.player.status()
            write("Pomme: {}".format(status.bombs), 0)
            write("Raadius: {}".format(status.bombRadius), 1)
            write("Kiirus: {}".format(status.speed), 2)
            write("Elusid: {}".format(status.lives), 3)
            height = self.boardSize-10
            for line in reversed(status.comment.split("\n")):
                height -= 30
                self.writeCentered(line, (x+self.panelSize//2, height), self.smallfont)
        if flip: 
            pygame.display.flip()
        
    def writeCentered(self, text, pos, font, color=(255,255,255)):
        " Writes something centered along the width axis "
        x,y = pos
        textWidth,_ = font.size(text)
        rendered = font.render(text, True, color)
        self.getScreen().blit(rendered, (x-textWidth//2, y))
        
    def winScreen(self, urmasLoses, katrinLoses):
        fade(3000)
        h = self.font.size("U")[1]
        self.urmas.wRect = self.urmas.rect.move(self.boardSize//2-30, -h+30)
        self.katrin.wRect = self.katrin.rect.move(-self.boardSize//2+30, -h+30)
        if urmasLoses and katrinLoses:
            self.katrin.stateCallback = lambda: SAD
            self.urmas.stateCallback = lambda: SAD
            self.showWinScreen("Viiki j2i. :)")
        elif urmasLoses:
            self.katrin.stateCallback = lambda: HAPPY
            self.urmas.stateCallback = lambda: SAD
            self.showWinScreen("Katrin on stuudio valitseja!")
        elif katrinLoses:
            self.katrin.stateCallback = lambda: SAD
            self.urmas.stateCallback = lambda: HAPPY
            self.showWinScreen("Urmas on stuudio valitseja!")
        fade(3000, reverse = True)
        
    def showWinScreen(self, winText):
        if not hasattr(self, "winimage"):
            self.winimage, self.winPos = getScaledCenteredImage(titleImagePath, 
                                                   self.boardSize + 2*self.panelSize, 
                                                   self.boardSize)
        self.screen.blit(self.winimage, self.winPos)
        center = self.panelSize + self.boardSize//2
        self.writeCentered(winText, (center, self.boardSize//2), self.font)
        for face in [self.katrin, self.urmas]:
            face.update()
            self.screen.blit(face.image, face.wRect)
        #pygame.display.flip()
        
    def resetScreen(self):
        screensize = self.screen.get_size()
        darken=pygame.Surface(screensize)
        darken.fill((0,0,0))
        self.screen.blit(darken,(0,0))
        
    def screenSize(self):
        return (self.boardSize + 2*self.panelSize, self.boardSize)
        
    
def getScaledCenteredImage(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    nWidth, nHeight = sizeMatch(image.get_width(), image.get_height(), width, height)
    image = pygame.transform.smoothscale(image, (nWidth, nHeight))
    return image, ((width - nWidth)//2, (height - nHeight)//2)

def sizeMatch(width1, height1, width2, height2):
    assert(width1 >= width2 and height1 >= height2)
    rW = 1.0 * width2 / width1
    rH = 1.0 * height2 / height1
    ratio = max(rW, rH)
    #print ratio, width1, height1, width2, height2, 1.0*width2 / width1, 1.0 * height2 / height1
    return (int(width1 * ratio), int(height1 * ratio))
    