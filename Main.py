# -*- coding: utf-8 -*-

import pygame
from Game import Game
from drawers.Face import Face
import sys
from misc import *
from pygame.locals import *

sys.path.append(".")

class Main(object):
    PANELWIDTH = 130
    def __init__(self, squareSize, mapSize):
        self.squareSize = squareSize
        self.mapSize = mapSize
        size = self.squareSize*self.mapSize
        
        pygame.init()
        self.screen = pygame.display.set_mode((size+2*self.PANELWIDTH, size))
        self.game = Game(self.screen, self.squareSize, self.mapSize, {"start_x":self.PANELWIDTH})
        self.urmas = Face(URMASPICS, (0,0,self.PANELWIDTH,self.PANELWIDTH), 
                          self.game.players[0].stateOfMind)
        self.katrin = Face(KATRINPICS, (self.PANELWIDTH+size,0,self.PANELWIDTH,self.PANELWIDTH), 
                           self.game.players[1].stateOfMind)
       
        
    def mainloop(self):
        self.clock = pygame.time.Clock()
        while True:
            self.tick()
            
    def tick(self):
        t = self.clock.tick(50)
        self.game.processEvents(t)
        self.game.update(t, False)
        self.urmas.update()
        self.katrin.update()
        self.screen.blit(self.urmas.image, self.urmas.rect)
        self.screen.blit(self.katrin.image, self.katrin.rect)
        pygame.display.flip()
        
            
            
if __name__ == "__main__":
    Main(25, 20).mainloop()
        