# TODO: image locations, amount to create, can be on top of stuff, method to do updates
import pygame
import sys
import os
sys.path.append(".")
from misc import *

tileFolder = os.path.join("resources","images","tiles")

class Tile(object):
    def __init__(self, imagePath, fragile = False, collectable = False, solid = True, amount = lambda s: 0):
        self.imagePath = imagePath
        self.fragile = fragile
        self.collectable = collectable
        self.solid = solid
        self.amount = amount
        
    def __call__(self, size):
        if not hasattr(self, "lastImage") or self.lastSize != size:
            if not hasattr(self, "image") :
                 self.image = pygame.image.load(self.imagePath).convert_alpha()
            image = pygame.transform.smoothscale(self.image, (size, size))
            image.set_colorkey((0,0,0))
            image.set_alpha(50)
            self.lastImage = image
            self.lastSize = size
            
        return self.lastImage
        
    @staticmethod
    def canGoUnder(cls): return False
    
class Collectable(Tile):
    fragile = False
    collectable = True
    solid = False
    def __init__(self, imagePath, collect, amount = lambda s: 0):
        self.imagePath = imagePath
        self.fragile = False
        self.collectable = True
        self.solid = False
        self.collectBy = collect
        self.amount = amount
    
    @staticmethod
    def canGoUnder(cls): 
        return cls.fragile and not isinstance(cls, Player)
        
Rock = Tile(os.path.join(tileFolder,"rock.png"), fragile=True, amount=lambda s:3*s)
Beam = Tile(imagePath = os.path.join(tileFolder,"beam.png"), amount=lambda s:4*s)
    
class TileConstructor(Tile):
    def __init__(self, imageName):
        self.imagePath = os.path.join(tileFolder,imageName)
    
    def getImage(self, size):
        if not hasattr(self, "lastImage") or self.lastSize != size:
            if not hasattr(self, "image"):
                 self.image = pygame.image.load(self.imagePath).convert_alpha()
            image = pygame.transform.smoothscale(self.image, (size, size))
            self.lastImage = image
            self.lastSize = size
        return self.lastImage
    
class Player(Tile):
    fragile = True
    def __init__(self, images):
        self.images = {
            NORTH: TileConstructor(images[0]),
            SOUTH: TileConstructor(images[1]),
            EAST: TileConstructor(images[2]),
            WEST:TileConstructor(images[3])
        }
        
    def getTile(self, direction):
        return self.images[direction]
        

BombTile = Tile(os.path.join(tileFolder,"Bomb.png"))
ExplosionTile = Tile(os.path.join(tileFolder,"explosion.png"))
Background = Tile(os.path.join("resources","images","background.png"))

def pepperCollect(player):
    player.bombRadius += 1
Pepper = Collectable(os.path.join(tileFolder,"pepper.png"), pepperCollect, lambda s: 5)

def bombCollect(player):
    player.bombs += 1
BombBonus = Collectable(os.path.join(tileFolder,"bombBonus.png"), bombCollect, lambda s: 5)

def collectCoffee(player):
    player.speed *= 1.6
Coffee = Collectable(os.path.join(tileFolder,"coffee.png"), collectCoffee, lambda s: 3)    
    
Player1 = Player(["p_1_up.png","p_1_down.png","p_1_right.png","p_1_left.png"])
Player2 = Player(["p_2_up.png","p_2_down.png","p_2_right.png","p_2_left.png"])
    
allObjects = [Rock, Beam]
players = [Player1, Player2]
placeable = [Rock, Beam, Pepper, BombBonus, Coffee]

if __name__ == "__main__":
    print allObjects
    pygame.init()
    size = 80
    screen = pygame.display.set_mode((size*len(allObjects), size))
    for i, el in enumerate(allObjects):
        screen.blit(el.getImage(size), (i*size, 0))
    pygame.display.flip()