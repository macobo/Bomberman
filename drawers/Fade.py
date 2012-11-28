# -*- coding: utf-8 -*-
import pygame

def fade(time, reverse = False, factor = 250):
    dimmer = Dimmer()
    dimmer.darken_factor = factor
    clock = pygame.time.Clock()
    t = 0
    while t < time:
        t += clock.tick(50)
        if not reverse:
            dimmer.darken(1.0 * t / time)
        else:
            dimmer.darken(1 - 1.0 * t / time)
        pygame.display.flip()
        dimmer.restore()
        
class Dimmer(object):
    darken_factor = 250
    filter = (0,0,0)
    def __init__(self):
        screen = pygame.display.get_surface()
        screensize = screen.get_size()
        self.buffer = pygame.Surface(screensize)
        self.buffer.blit(screen, (0,0))
        
    def darken(self, factor):
        #print factor * self.darken_factor
        screen = pygame.display.get_surface()
        screensize = screen.get_size()
        self.buffer = pygame.Surface(screensize)
        self.buffer.blit(screen, (0,0)) # to restore later
        darken=pygame.Surface(screensize)
        darken.fill(self.filter)
        darken.set_alpha(factor * self.darken_factor)
        # safe old clipping rectangle...
        old_clip = screen.get_clip()
        # ..blit over entire screen...
        screen.blit(darken, (0,0))
        # ... and restore clipping
        screen.set_clip(old_clip)
##        pygame.display.flip()
        
    def restore(self):
        #print self.buffer
        pygame.display.get_surface().blit(self.buffer,(0,0))
        #self.buffer = None