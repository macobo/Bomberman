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
    STARTSPEED = 0.005
    STARTRADIUS = 2
    STARTBOMBS = 2
    SPEEDINCCONSTANT = 1.3
    
    def __init__(self, tile, x, y):
        self.neutral_x = x
        self.neutral_y = y
        self.x, self.y = x, y
        self.tile = tile
        self.direction = NORTH
        self.lives = 1000
        self.dead = False
        self.speed = 0.005
        self.bombRadius = 2
        self.bombs = 2
        self.placed = 0
        self.reset()
    
    def toNeutralCorner(self):
        self.x, self.y = self.neutral_x, self.neutral_y
        
    def reset(self):
        self.vx = self.vy = 0
        self.comment = ""
        self.lastKill = self.lastBonus = self.LASTKILLTIME
        
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
            self.bombs = max(self.STARTBOMBS, self.bombs - 1)
            self.bombRadius = max(self.STARTRADIUS, self.bombRadius - 1)
            self.speed = max(self.STARTSPEED, self.speed / self.SPEEDINCCONSTANT)
            self.reset()
            return True
        return False
            
    
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
        self.lastBonus += t
        if self.lastKill > self.LASTKILLTIME:
            self.comment = ""
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
        
    def resetKillCounter(self, suicide = False):
        self.lastKill = 0
        if suicide:
            self.comment = random.choice(SUICIDECOMMENTS)
        else:
            self.comment = random.choice(COMMENTS)
        
    def resetBonusCounter(self):
        self.lastBonus = 0

    def stateOfMind(self):
        xy = self.getRoundCoordinate()
        if self.dead or any(xy in bomb.inRange(self.map) for bomb in self.map.bombs):
            return SAD
        if self.lastKill < self.LASTKILLTIME:
            return HAPPY
        if self.lastBonus < self.LASTKILLTIME:
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