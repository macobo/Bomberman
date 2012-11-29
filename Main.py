# -*- coding: utf-8 -*-

import pygame
from Game import Game
from drawers.PanelDrawer import PanelDrawer
from drawers.TitleScreen import initScreen
from drawers.Fade import fade
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
        
    def initScreen(self):
        self.game.update(0, False)
        self.panel.update(False)
        lives = initScreen(*self.panel.screenSize())
        for player in self.game.players:
            player.lives = lives
        fade(1000)
        self.panel.resetScreen()
        self.panel.writeNames()
        self.panel.update(flip = False)
        self.game.redraw(update = False)
        fade(2500, reverse = True)
        
        
    def mainloop(self):
        self.panel.writeNames()
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
            fade(1500)
            for player in self.game.players:
                player.toNeutralCorner()
            self.game.map.resetMap(regen = True)
            self.game.redraw(update = False)
            fade(1500, reverse = True)
            self.clock.tick(100)
        self.panel.update()
        return t
            
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pommimäng")
    main = Main(25, 20)
    main.initScreen()
    main.mainloop()