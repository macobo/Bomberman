# -*- coding: utf-8 -*-

import pygame
from Game import Game
from drawers.PanelDrawer import PanelDrawer
import sys
from misc import *
from pygame.locals import *

sys.path.append(".")

class Main(object):
    PANELWIDTH = 160
    def __init__(self, squareSize, mapSize):
        self.squareSize = squareSize
        self.mapSize = mapSize
        size = self.squareSize*self.mapSize
        self.panel = PanelDrawer(self.PANELWIDTH, size)
        self.game = Game(self.panel.getScreen(), self.squareSize, self.mapSize, {"start_x":self.PANELWIDTH})
        self.panel.createFaces(self.game.map)
        
    def mainloop(self):
        self.clock = pygame.time.Clock()
        while True:
            self.tick()
                
            
    def tick(self):
        t = self.clock.tick(50)
        self.game.processEvents(t)
        if self.game.update(t, False) and not self.game.map.thingsLeft():
            self.game.map.resetMap(regen = True)
        self.panel.update()
            
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pommimäng")
    Main(25, 20).mainloop()