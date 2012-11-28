# -*- coding: utf-8 -*-

import pygame, sys
sys.path.append(".")
from misc import *
from drawers.Face import Face

class PanelDrawer(object):

    def __init__(self, panelSize, boardSize):
        self.panelSize = panelSize
        self.boardSize = boardSize
        self.getScreen()
        self.font = pygame.font.Font(fontPath, 40)
        self.smallfont = pygame.font.Font(fontPath, 20)
        
    def createFaces(self, map):
        self.writeCentered("Urmas", (self.panelSize//2, 0), self.font)
        self.h = self.font.size("U")[1]
        self.urmas = Face(URMASPICS, (0,self.h,
                                      self.panelSize,self.panelSize), 
                           map.players[0])
        self.writeCentered("Katrin", (3*self.panelSize//2+self.boardSize, 0), self.font)
        self.katrin = Face(KATRINPICS, (self.panelSize+self.boardSize,self.h,
                                        self.panelSize,self.panelSize), 
                           map.players[1])
        self.katrin.update()
        self.faces = [(self.urmas, (0, 0)),
                      (self.katrin, (self.panelSize+self.boardSize, 0))]
        self.h += self.katrin.image.get_height()
        
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