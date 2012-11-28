# -*- coding: utf-8 -*-

from collections import namedtuple
from misc import *
from math import trunc
import random

class Player:
    TOTALDEADTIME = 3000
    LASTKILLTIME = 1500
    statusTuple = namedtuple("Status", ["speed", "bombs", "bombRadius", "lives", "comment"])
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
        self.speed = 0.005
        self.bombRadius = 2
        self.bombs = 2
        self.placed = 0
        self.comment = ""
        self.reset()
        
    def reset(self):
        self.vx = self.vy = 0
        
    def canPlaceBomb(self):
        assert(0 <= self.placed <= self.bombs)
        return not self.dead and self.placed < self.bombs
        
    def placeBomb(self):
        assert(0 <= self.placed < self.bombs)
        self.placed += 1
    
    def addBomb(self):
        assert(1 <= self.placed)
        assert(self.placed <= self.bombs)
        self.placed = self.placed-1 # can occur when you die
        
    def die(self):
        self.deadTime = 0
        if not self.dead:
            self.dead = True
            self.lives -= 1
            self.reset()
            
    
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
            if self.lastKill > self.LASTKILLTIME:
                self.comment = ""
        
    def setDirection(self, direction):
        if self.dead: 
            return
        x, y = direction
        self.vx = x * self.speed
        self.vy = y * self.speed
        self.direction = direction
        
    def resetHappyCounter(self):
        self.lastKill = 0
        self.comment = random.choice(COMMENTS)

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
                                 lives = self.lives,
                                 comment = self.comment))
    
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