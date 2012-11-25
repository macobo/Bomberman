# -*- coding: utf-8 -*-

from misc import *

class Player:
    def __init__(self, tile):
        self.x = self.y = 0
        self.vx = self.vy = 0
        self.speed = 0.005
        self.tile = tile
        self.direction = NORTH
        
    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def getPos(self):
        return (self.x, self.y)
        
    def setMovement(self, vxy):
        self.vx, self.vy = vxy
    
    def move(self, t):
        """ Calculates new position of tile after t seconds of pause """
        self.x += self.vx * t
        self.y += self.vy * t
        
    def setDirection(self, direction):
        x, y = direction
        self.vx = x * self.speed
        self.vy = y * self.speed
        self.direction = direction
    
    def getTile(self):
        return self.tile.getTile(self.direction)
    
    def setMap(self, model):
        self.map = model
        
    def __repr__(self):
        return str(self.getPos())