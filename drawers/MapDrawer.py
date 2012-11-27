import pygame
from models import Objects

class MapDrawer(object):
    def __init__(self, model, screen, tileSize, mapSize, start_x=0, start_y=0):
        self.model = model
        self.screen = screen
        self.tileSize = tileSize
        self.mapSize = mapSize
        self.start_x = start_x
        self.start_y = start_y

    def adjusted(self, row, col, w = None, h = None):
        """Adjusts the row and column to map to coordinates on screen"""
        dw = 0 if w is None else self.tileSize - w
        dh = 0 if h is None else self.tileSize - h
        return (row * self.tileSize + self.start_x + dw / 2, 
                col * self.tileSize + self.start_y + dh / 2)
        
    def redraw(self, update = True):
        """ Redraws the map onto the screen. If update is True, 
            pygame.display.flip() will be called. """
        self.screen.blit(Objects.Background(self.tileSize*self.mapSize), (self.start_x, self.start_y))
        for (row, col), tile in self.model.items():
            icon = tile(self.tileSize)
            w, h = icon.get_size()
            self.screen.blit(icon, self.adjusted(row, col, w, h))
        if update:
            pygame.display.flip()

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from models.MapModel import MapModel
    n = 20
    model = MapModel(n)
    pygame.init()
    size = 25
    screen = pygame.display.set_mode((size*n, size*n))
    drawer = MapDrawer(model, screen, size)
    drawer.redraw()
    pygame.time.delay(3000)