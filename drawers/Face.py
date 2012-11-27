import pygame
class Face(pygame.sprite.Sprite):
    def __init__(self, imagePaths, rect, player):
        pygame.sprite.Sprite.__init__(self)
        self.imagePath = imagePaths
        self.images = {}
        self.rect = pygame.Rect(rect)
        self.player = player
        self.stateCallback = player.stateOfMind
    
    def update(self):
        state = self.stateCallback()
        if state not in self.images:
            self.images[state] = pygame.image.load(self.imagePath[state]).convert_alpha()
            iwidth, iheight = self.images[state].get_size()
            width = self.rect.width
            height = int(1.0 * width / iwidth  * iheight)
            self.images[state] = pygame.transform.smoothscale(self.images[state], (width, height))
        self.image = self.images[state]
    
    def setCallback(self, cb):
        self.stateCallback = cb