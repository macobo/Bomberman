# -*- coding: utf-8 -*-

from Objects import Tile, BombTile

class Bomb(Tile):
    EXPLODETIME = 3000
    def __init__(self, x, y, player):
        Tile.__init__(self, None)
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
        
    def __call__(self, size):
        mul = min(0.4 + 0.6 * self.time / self.EXPLODETIME,1.3)
        return BombTile(int(round(size * mul)))
    
    # TODO: inRange(player)