# -*- coding: utf-8 -*-

from misc import *
from math import trunc

class Player(object):
    TOTALDEADTIME = 3000
    def __init__(self, tile, x, y):
        self.x = x
        self.y = y
        self.tile = tile
        self.direction = NORTH
        self.reset()
        
    def reset(self):
        self.vx = self.vy = 0
        self.speed = 0.005
        self.bombRadius = 3
        self.bombs = 1
        self.placed = 0
        self.dead = False
        
    def canPlaceBomb(self):
        return not self.dead and self.placed < self.bombs
        
    def placeBomb(self):
        self.placed += 1
    
    def addBomb(self):
        self.placed = min(1, self.placed-1) # can occur when you die
        
    def die(self):
        self.dead = True
        self.deadTime = 0
    
    def setMap(self, mapModel):
        self.map = mapModel
        
    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def getPos(self):
        return (self.x, self.y)
        
    def getRoundCoordinate(self):
        return self.round(self.x, self.y)
        
    def setMovement(self, vxy):
        self.vx, self.vy = vxy
    
    def tick(self, t):
        """ Calculates new position of tile after t seconds of pause """
        if not self.dead:
            self.x, self.y = self.map.move(self, t)
        else:
            self.deadTime += t
            if self.deadTime > self.TOTALDEADTIME:
                self.reset()
        
    def setDirection(self, direction):
        if self.dead: return
        x, y = direction
        self.vx = x * self.speed
        self.vy = y * self.speed
        self.direction = direction
    
    def getTile(self):
        tile = self.tile.getTile(self.direction)
        return tile

    def stateOfMind(self):
        status = NEUTRAL
        return status
    
    def __repr__(self):
        return str(self.getPos())
        
    @staticmethod
    def round(x, y):
        y = int(y) if y-trunc(y) < 0.2 else int(y)+1
        x = int(round(x))
        return x, y