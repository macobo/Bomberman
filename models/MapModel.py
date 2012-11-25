import Objects
from Player import Player
import random
from collections import defaultdict

class MapModel(object):
    def __init__(self, size, *players):
        assert(size > 10)
        self.size = size
        self.players = players
        self._generateMap()

    def items(self):
        """ Returns all objects in the map. Bonuses will be before rocks and players will be last """
        from itertools import product
        for xy in product(range(self.size), repeat=2):
            if xy in self.map:
                for tile in self.map[xy]:
                    yield xy, tile
            else:
                yield xy, Objects.Floor
        for player in self.players:
            yield player.getPos(), player.getTile()
        
    def _generateMap(self):
        self.map = defaultdict(list)
        for obj in Objects.placeable:
            placed = 0
            while placed < obj.amount(self.size):
                (x, y) = random.randrange(self.size), random.randrange(self.size)
                canPlace = (x, y) not in self.map
                canPlace = canPlace or all(obj.canGoUnder(x) for x in self.map[x,y])
                if canPlace:
                    self.map[x,y].append(obj)
                    placed += 1

    def __str__(self):
        out = ["Map of {0}x{0}".format(self.size)]
        for row in range(self.size):
            s = []
            for col in range(self.size):
                s.append('0' if (row, col) not in self.map else self.map[row,col][0].symbol)
            out.append(" ".join(s))
        return "\n\n".join(out)
        
    def objectsAt(self, x, y):
        """ Returns tiles for objects at coordinate x,y """
        x, y = Player.round(x,y)
        result = []
        for xy, tile in self.map.items():
            if xy == (x,y):
                result.append(tile)
        return result
        
    def playersAt(self, xy):
        return filter(lambda p: p.getRoundPos()==xy, self.players)
        
    def move(self, player, t):
        """ Tries to move player and returns new coordinates for it """
        nx = inRange(player.x + player.vx * t, self.size-1)
        ny = inRange(player.y + player.vy * t, self.size-1)
        if self.objectsAt(nx, ny):
            return player.x, player.y
        return nx, ny
        
        

def inRange(x, upper, lower=0):
    " returna either x, or a number in range [upper, lower] in according end"
    return max(min(x, upper), lower)    
    
if __name__ == "__main__":
    m = MapModel(11)
    print(m)