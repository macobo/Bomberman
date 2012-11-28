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
        for xy, tiles in self.map.items():
            for tile in tiles:
                yield xy, tile
        for player in self.players:
            yield player.getPos(), player.getTile()
        for explosion in self.explosions:
            for xy in explosion.getAffected():
                yield xy, explosion
    
    def remove(self, obj, xy):
        xy = Player.round(*xy)
        self.map[xy].remove(obj)
        if not self.map[xy]:
            del self.map[xy]
            
    def add(self, obj, xy):
        xy = Player.round(*xy)
        self.map[xy].append(obj)
        
    def _generateMap(self):
        self.map = defaultdict(list)
        for obj in Objects.placeable:
            placed = 0
            while placed < obj.amount(self.size):
                (x, y) = random.randrange(self.size), random.randrange(self.size)
                here = self.objectsAt((x,y))
                canPlace = (x, y) not in self.map
                canPlace = canPlace or all(obj.canGoUnder(x) for x in here)
                canPlace = canPlace and (not obj.collectable or (bool(here) and all(x.fragile for x in here)))
                if canPlace:
                    self.add(obj, (x,y))
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
        result = self.map[x,y] if (x,y) in self.map else []
        assert(not any(isinstance(x, Player) for x in result))
        return result
        
    def playersAt(self, xy):
        xy = Player.round(*xy)
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
        objects = self.objectsAt((nx, ny))
        players = list(self.playersAt((nx, ny)))
        if len(players) > 1:
            players.remove(player)
            objects = objects + players
        cannotMove = bool(objects)
        cannotMove = cannotMove and any(x.solid for x in objects)
        # cannot step through
        ox, oy = Player.round(nx, ny)
        if objects and len(objects) == 1 and isinstance(objects[0], Bomb):
            ox, oy = objects[0].getPos()
        cannotMove = cannotMove and abs(ox-nx) <= abs(ox-player.x)
        cannotMove = cannotMove and abs(oy-ny) <= abs(oy-player.y)
        if cannotMove:
            return player.x, player.y
        return nx, ny
        

    
    def placeBomb(self, player):
        x, y = player.getPos()
        pos = player.getRoundCoordinate()
        if pos in self.map or not player.canPlaceBomb(): 
            return
        player.placeBomb()
        bomb = Bomb(x, y, player)
        assert(not isinstance(bomb, Player))
        self.bombs.append(bomb)
        self.add(bomb, pos)
        print "Placed a bomb at",x,y
        
        
    def explode(self, bomb):
        # out with the old
        self.bombs.remove(bomb)
        self.remove(bomb, bomb.getPos())
        bomb.player.addBomb()
        # in with the new
        explosion = Explosion(bomb, self)
        affected = explosion.getAffected()
        for xy in filter(self.map.has_key, affected):
            self.map[xy] = filter(lambda x: not x.fragile, self.map[xy])
            if not self.map[xy]: 
                del self.map[xy]
        for xy in filter(self.playersAt, affected):
            for player in self.playersAt(xy):
                print "{} dies".format(player)
                player.die()
                bomb.player.resetHappyCounter()
        self.explosions.append(explosion)
        

def inRange(x, upper, lower=0):
    " returna either x, or a number in range [upper, lower] in according end"
    return max(min(x, upper), lower)    
    
if __name__ == "__main__":
    m = MapModel(11)
    print(m)