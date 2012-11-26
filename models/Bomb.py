# -*- coding: utf-8 -*-

from Objects import BombTile

class Bomb(BombTile):
    ignoreBomb = True
    
    EXPLODETIME = 3000
    def __init__(self, x, y, player):
        self.x, self.y = x, y
        self.radius = player.bombRadius
        self.time = 0
        self.player = player
        
    def getPos(self):
        return self.x, self.y
        
    def tick(self, t):
        " Returns true if bomb is ready to explode "
        self.time += t
        return self.time >= self.EXPLODETIME
        
    def getImage(self, size):
        mul = min(0.4 + 0.6 * self.time / self.EXPLODETIME,1.3)
        return BombTile.getImage(int(round(size * mul)))
    
    # TODO: inRange(player)