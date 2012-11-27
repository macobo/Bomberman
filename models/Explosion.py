# -*- coding: utf-8 -*-
from misc import *
from Objects import ExplosionTile, Tile
from Player import Player

class Explosion(Tile):
    EXPLOSIONTIME = 700
    def __init__(self, bomb, map):
        Tile.__init__(self, None, solid = False)
        x, y = bomb.getPos()
        self.affected = calculateAffected(bomb, map)
        self.time = 0
        
    def getAffected(self):
        return self.affected
    
    def tick(self, t):
        self.time += t
        return self.time > self.EXPLOSIONTIME
        
    def __call__(self, size):
        mul = min(1.5, 0.4 + 0.6 * self.time / self.EXPLOSIONTIME)
        return ExplosionTile(int(round(size * mul)))


def calculateAffected(bomb, map):
    " Calculates the (x,y) positions of affected squares "
    ax, ay = Player.round(*bomb.getPos())
    radius = bomb.radius
    affected = set()
    for dx, dy in DIRECTIONS:
        for i in range(radius+1):
            x = ax + i*dx
            y = ay + i*dy
            if not (0 <= x < map.size) or not (0 <= y < map.size):
                continue
            objects = map.objectsAt((x,y))
            if objects and any(obj.solid and not isinstance(obj, bomb.__class__) for obj in objects):
                if any(obj.fragile for obj in objects):
                    affected.add((x, y))
                break
            affected.add((x, y))
    return affected