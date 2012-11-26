# -*- coding: utf-8 -*-
from misc import *
from Objects import ExplosionTile

class Explosion(ExplosionTile):
    EXPLOSIONTIME = 700
    def __init__(self, bomb, map):
        x, y = bomb.getPos()
        self.affected = calculateAffected(x,y, map, bomb.radius)
        self.time = 0
        
    def getAffected(self):
        return self.affected
    
    def tick(self, t):
        self.time += t
        return self.time > self.EXPLOSIONTIME
        
    def getImage(self, size):
        mul = min(1.5, 0.4 + 0.6 * self.time / self.EXPLOSIONTIME)
        return ExplosionTile.getImage(int(round(size * mul)))


def calculateAffected(x, y, map, radius):
    " Calculates the (x,y) positions of affected squares "
    affected = set()
    for dx, dy in DIRECTIONS:
        for i in range(radius+1):
            objects = map.objectsAt((x + i*dx, y + i*dy))
            if objects and any(obj.solid for obj in objects):
                if any(obj.fragile for obj in objects):
                    affected.add((x+i*dx, y+i*dy))
                break
            affected.add((x+i*dx, y+i*dy))
    return affected