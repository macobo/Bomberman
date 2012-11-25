# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
from models.MapModel import MapModel
from drawers.MapDrawer import MapDrawer
from models.Player import Player
from models import Objects
from misc import *

class Game:
    def __init__(self, screen, squareSize = 30, size = 20):
        self.screen = screen
        self.player1 = Player(Objects.Player1)
        self.map = MapModel(size, self.player1)
        self.player1.setMap(self.map)
        self.drawer = MapDrawer(self.map, screen, squareSize)
        
    
    def redraw(self, update = True):
        self.drawer.redraw(update)
    
    def processEvents(self, t):
        """ Processes events, taking into account t seconds have passed since last """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
        
        keys = pygame.key.get_pressed()
        pressed = 0
        tdirection = (0,9)
        for key, direction in zip(KEYS, DIRECTIONS):
            if keys[key]:
                pressed += 1
                tdirection = direction
        if pressed != 1:
            self.player1.setMovement((0,0))
        else:
            self.player1.setMovement(tdirection)
            self.player1.setDirection(tdirection)
    
    def update(self, t):
        self.player1.move(t)
        self.redraw()
        
        
        
if __name__ == "__main__":
    
    sys.path.append(".")
    n = 20
    pygame.init()
    size = 25
    screen = pygame.display.set_mode((size*n, size*n))
    game = Game(screen, size, n)
    clock = pygame.time.Clock()
    while True:
        t = clock.tick(40)
        game.processEvents(t)
        game.update(t)