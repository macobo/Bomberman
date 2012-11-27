# -*- coding: utf-8 -*-

from collections import namedtuple
from Objects import Tile
from misc import *
from math import trunc

class Player:
    TOTALDEADTIME = 3000
    LASTKILLTIME = 1500
    statusTuple = namedtuple("Status", ["speed", "bombs", "bombRadius", "lives"])
    solid = True
    collectable = False
    
    def __init__(self, tile, x, y):
        self.x = x
        self.y = y
        self.tile = tile
        self.direction = NORTH
        self.lives = 4
        self.dead = False
        self.lastKill = self.LASTKILLTIME
        self.reset()
        
    def reset(self):
        self.vx = self.vy = 0
        self.speed = 0.005
        self.bombRadius = 2
        self.bombs = 1
        self.placed = 0
        
    def canPlaceBomb(self):
        return not self.dead and self.placed < self.bombs
        
    def placeBomb(self):
        self.placed += 1
    
    def addBomb(self):
        self.placed = min(1, self.placed-1) # can occur when you die
        
    def die(self):
        self.dead = True
        self.lives -= 1
        self.reset()
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
        self.lastKill += t
        if not self.dead:
            self.x, self.y = self.map.move(self, t)
        else:
            self.deadTime += t
            if self.deadTime > self.TOTALDEADTIME:
                self.dead = False
        
    def setDirection(self, direction):
        if self.dead: 
            return
        x, y = direction
        self.vx = x * self.speed
        self.vy = y * self.speed
        self.direction = direction
        
    def resetHappyCounter(self):
        self.lastKill = 0

    def stateOfMind(self):
        xy = self.getRoundCoordinate()
        if self.dead or any(xy in bomb.inRange(self.map) for bomb in self.map.bombs):
            return SAD
        if self.lastKill < self.LASTKILLTIME:
            return HAPPY
        return NORMAL
        
    def status(self):
        return (self.statusTuple(speed = round(self.speed*200,2),
                                 bombs = self.bombs,
                                 bombRadius = self.bombRadius,
                                 lives = self.lives))
    
    def __repr__(self):
        return "Player at {}".format(self.getPos())
        
    def getTile(self):
        tile = self.tile.getTile(self.direction)
        return tile
        
    @staticmethod
    def round(x, y):
        y = int(y) if y-trunc(y) < 0.2 else int(y)+1
        x = int(round(x))
        return x, y