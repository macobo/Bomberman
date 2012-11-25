import pygame

class MapDrawer(object):
    def __init__(self, model, screen, tileSize, start_x=0, start_y=0):
        self.model = model
        self.screen = screen
        self.tileSize = tileSize
        self.start_x = start_x
        self.start_y = start_y

    def adjusted(self, row, col):
        """Adjusts the row and column to map to coordinates on screen"""
        return (row * self.tileSize + self.start_x, 
                col * self.tileSize + self.start_y)
        
    def redraw(self, update = True):
        """ Redraws the map onto the screen. If update is True, 
            pygame.display.flip() will be called. """
        for (row, col), tile in self.model.items():
            icon = tile.getImage(self.tileSize)
            self.screen.blit(icon, self.adjusted(row, col))
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