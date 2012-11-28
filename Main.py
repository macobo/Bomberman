# -*- coding: utf-8 -*-

import pygame
from Game import Game
from drawers.PanelDrawer import PanelDrawer
import sys
from misc import *
from pygame.locals import *

sys.path.append(".")

class Main(object):
    PANELWIDTH = 165
    def __init__(self, squareSize, mapSize):
        self.squareSize = squareSize
        self.mapSize = mapSize
        size = self.squareSize*self.mapSize
        self.panel = PanelDrawer(self.PANELWIDTH, size)
        self.game = Game(self.panel.getScreen(), self.squareSize, self.mapSize, {"start_x":self.PANELWIDTH})
        self.panel.createFaces(self.game.map)
        
    def mainloop(self):
        self.clock = pygame.time.Clock()
        while not self.game.winners():
            self.tick()
        winners = self.game.winners()
        self.panel.winScreen(*[p in winners for p in self.game.players])
        pygame.time.delay(5000)
            
            
    def tick(self):
        t = self.clock.tick(50)
        self.game.processEvents(t)
        if self.game.update(t, False) and not self.game.map.thingsLeft():
            self.panel.fade(1500)
            for player in self.game.players:
                player.toNeutralCorner()
            self.game.map.resetMap(regen = True)
            self.game.redraw(update = False)
            self.panel.fade(1500, reverse = True)
        self.panel.update()
        return t
            
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pommimäng")
    Main(25, 20).mainloop()