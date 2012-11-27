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
        self.player1 = Player(Objects.Player1, 0, 0)
        self.player2 = Player(Objects.Player1, size-1, size-1)
        self.map = MapModel(size, self.player1, self.player2)
        self.player1.setMap(self.map)
        self.player2.setMap(self.map)
        self.drawer = MapDrawer(self.map, screen, squareSize, size)
    
    def redraw(self, update = True):
        self.drawer.redraw(update)
    
    def processEvents(self, t):
        """ Processes events, taking into account t seconds have passed since last """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN and event.key == K_t:
                print("CHEAT")
                Objects.BombBonus.collectBy(self.player1)
                Objects.Pepper.collectBy(self.player1)
        self.handleKeys(self.player1, t, P1_KEYS)
        self.handleKeys(self.player2, t, P2_KEYS)
            
    def handleKeys(self, player, t, playerKeys):
        keys = pygame.key.get_pressed()
        pressed = 0
        newDirection = (0,0)
        for key, direction in zip(playerKeys[:-1], DIRECTIONS):
            if keys[key]:
                pressed += 1
                newDirection = direction
        if keys[playerKeys[-1]]:
            self.map.placeBomb(player)
        if pressed != 1:
            player.setMovement((0,0))
        else:
            player.setMovement(newDirection)
            player.setDirection(newDirection)
    
    def update(self, t):
        self.map.update(t)
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
        t = clock.tick(50)
        game.processEvents(t)
        game.update(t)
        #print game.player1.getRoundCoordinate()