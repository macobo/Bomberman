# TODO: image locations, amount to create, can be on top of stuff, method to do updates
import pygame
import sys
import os
sys.path.append(".")
from misc import *

tileFolder = os.path.join("resources","images","tiles")

class Tile(object):
    ignoreBomb = False
    fragile = False
    collectable = False
    @classmethod
    def getImage(cls, size):
        if not hasattr(cls, "lastImage") or cls.lastSize != size:
            if not hasattr(cls, "image") :
                 cls.image = pygame.image.load(cls.imagePath).convert_alpha()
            image = pygame.transform.smoothscale(cls.image, (size, size))
            cls.lastImage = image
            cls.lastSize = size
        return cls.lastImage
        
    @staticmethod
    def canGoUnder(cls): return False

class Rock(Tile):
    fragile = True
    symbol = "R"
    imagePath = os.path.join(tileFolder,"rock.png")

    @staticmethod
    def amount(size): return 3 * size

class Beam(Tile):
    fragile = False
    collectable = False
    symbol = "#"
    imagePath = os.path.join(tileFolder,"beam.png")

    @staticmethod
    def amount(size): return 4 * size

class Floor(Tile):
    imagePath = os.path.join(tileFolder,"floor.png")
    
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
        

class BombTile(Tile):
    symbol = "B"
    imagePath = os.path.join(tileFolder,"Bomb.png")
    
class ExplosionTile(Tile):
    imagePath = os.path.join(tileFolder,"explosion.png")
    
class Background(Tile):
    imagePath = os.path.join("resources","images","background.png")
    
    
Player1 = Player(["p_1_up.png","p_1_down.png","p_1_right.png","p_1_left.png"])
Player2 = Player(["p_2_up.png","p_2_down.png","p_2_right.png","p_2_left.png"])
    
allObjects = [Rock, Beam, Floor]
players = [Player1, Player2]
placeable = [Rock, Beam]

if __name__ == "__main__":
    print allObjects
    pygame.init()
    size = 80
    screen = pygame.display.set_mode((size*len(allObjects), size))
    for i, el in enumerate(allObjects):
        screen.blit(el.getImage(size), (i*size, 0))
    pygame.display.flip()