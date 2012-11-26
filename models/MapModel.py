import Objects
from Player import Player
from Bomb import Bomb
from Explosion import Explosion
import random
from collections import defaultdict

class MapModel(object):
    def __init__(self, size, *players):
        assert(size > 10)
        self.size = size
        self.players = players
        self.bombs = []
        self.explosions = []
        self._generateMap()

    def items(self):
        """ Returns all objects in the map. Bonuses will be before rocks and players will be last """
        from itertools import product
        for xy in product(range(self.size), repeat=2):
            if xy in self.map:
                for tile in self.map[xy]:
                    yield xy, tile
            #else:
            #    yield xy, Objects.Floor
        for player in self.players:
            yield player.getPos(), player.getTile()
        for explosion in self.explosions:
            for xy in explosion.getAffected():
                yield xy, explosion
    
    def remove(self, obj, xy):
        self.map[xy].remove(obj)
        if not self.map[xy]:
            del self.map[xy]
        
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
        
    def objectsAt(self, xy):
        """ Returns tiles for objects at coordinate x,y """
        x, y = Player.round(*xy)
        return self.map[x,y] if (x,y) in self.map else None
        
    def playersAt(self, xy):
        return filter(lambda p: p.getRoundCoordinate()==xy, self.players)
        
    def update(self, t):
        for player in self.players:
            player.tick(t)
            xy = player.getRoundCoordinate()
            if xy not in self.map: continue
            for collectable in filter(lambda x: x.collectable, self.map[xy]):
                collectable.collectBy(player)
                self.remove(collectable, xy)
            
        for bomb in self.bombs[:]:
            if bomb.tick(t):
                print "BOOM", bomb.time
                self.explode(bomb)
        for explosion in self.explosions[:]:
            if explosion.tick(t):
                self.explosions.remove(explosion)
        
    def move(self, player, t):
        """ Tries to move player and returns new coordinates for it """
        nx = inRange(player.x + player.vx * t, self.size-1)
        ny = inRange(player.y + player.vy * t, self.size-1)
        cannotMove = bool(self.objectsAt((nx, ny)))
        cannotMove = cannotMove and any(x.solid for x in self.objectsAt((nx, ny)))
        # cannot step through
        ox, oy = Player.round(nx, ny)
        cannotMove = cannotMove and abs(ox - nx) <= abs(ox - player.x)
        cannotMove = cannotMove and abs(oy-ny) <= abs(oy-player.y)
        if cannotMove:
            return player.x, player.y
        return nx, ny
        

    
    def placeBomb(self, player):
        x, y = player.getRoundCoordinate()
        if (x,y) in self.map or not player.canPlaceBomb(): 
            return
        player.placeBomb()
        bomb = Bomb(x, y, player)
        self.bombs.append(bomb)
        self.map[x,y].append(bomb)
        print "Placed a bomb at ",x,y
        
        
    def explode(self, bomb):
        # out with the old
        self.bombs.remove(bomb)
        self.remove(bomb, bomb.getPos())
        bomb.player.explode()
        # in with the new
        explosion = Explosion(bomb, self)
        affected = explosion.getAffected()
        for xy in filter(self.map.has_key, affected):
            self.map[xy] = filter(lambda x: not x.fragile, self.map[xy])
            if not self.map[xy]: del self.map[xy]
        for xy in filter(self.playersAt, affected):
            # TODO: blow up player            
            pass
        self.explosions.append(explosion)
        
        

def inRange(x, upper, lower=0):
    " returna either x, or a number in range [upper, lower] in according end"
    return max(min(x, upper), lower)    
    
if __name__ == "__main__":
    m = MapModel(11)
    print(m)