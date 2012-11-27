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
        
    def createFaces(self, map):
        self.writeCentered("Urmas", (self.panelSize//2, 0))
        _,h = self.font.size("U")
        self.urmas = Face(URMASPICS, (0,h,
                                      self.panelSize,self.panelSize), 
                           map.players[0].stateOfMind)
        self.writeCentered("Katrin", (3*self.panelSize//2+self.boardSize, 0))
        self.katrin = Face(KATRINPICS, (self.panelSize+self.boardSize,h,
                                        self.panelSize,self.panelSize), 
                           map.players[1].stateOfMind)
        
    def getScreen(self):
        if not hasattr(self, "screen"):
            pygame.init()
            self.screen = pygame.display.set_mode((self.boardSize+2*self.panelSize, 
                                                   self.boardSize))
        return self.screen
        
    def update(self, flip=True):
        self.urmas.update()
        self.katrin.update()
        self.getScreen().blit(self.urmas.image, self.urmas.rect)
        self.getScreen().blit(self.katrin.image, self.katrin.rect)
        if flip: pygame.display.flip()
        
    def writeCentered(self, text, pos, color=(255,255,255)):
        " Writes something centered along the width axis "
        x,y = pos
        textWidth,_ = self.font.size(text)
        rendered = self.font.render(text, True, color)
        self.getScreen().blit(rendered, (x-textWidth//2, y))