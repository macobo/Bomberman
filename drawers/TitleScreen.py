# -*- coding: utf-8 -*-
from Fade import Dimmer
import pygame
from misc import *
import sys

white = (255,255,255)
red = (255,0,0)
def putCenter(surface, width, height):
    w = surface.get_width()
    pygame.display.get_surface().blit(surface, ((width-w)//2, height))
    
def centerPos(surface, width, height, quarter, quarters):
    this = int(width / quarters * quarter)
    return (this - surface.get_width()//2, height)

def initScreen(width, height):
    dimmer = Dimmer()
    dimmer.darken(0.7)
    font = pygame.font.Font(fontPath, 40)
    smallfont = pygame.font.Font(fontPath, 20)
    putCenter(font.render("Pommim2ng", True, white), width, 20)
    putCenter(smallfont.render("Pommi panekuks on CTRL nupp, juhtimiseks:", True, white), width, 90)
    putCenter(smallfont.render("Vali, mitu elu teil on:", True, white), width, 320)
    
    image = pygame.image.load(arrowImagePath).convert_alpha()    
    putCenter(image, width, 100)
    
    colors = (white, red)
    h = 380
    
    numbers = ["3", "8", "12", "20"]
    hoverable = []
    screenBackup = Dimmer()
    for i,state in enumerate(numbers):
        states = [font.render(state, True, col) for col in colors]
        pos = centerPos(states[0], width, h, i+3, len(numbers)+5)
        hoverable.append(Hoverable(pos, HAT_CENTERED, *states))
        hoverable[-1].draw(0)
    
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                screenBackup.restore()
                pos = pygame.mouse.get_pos()
                for hov in hoverable:
                    if pos in hov:
                        hov.draw(1)
                    else:
                        hov.draw(0)
                pygame.display.flip()
            elif event.type == MOUSEBUTTONDOWN:
                for number, hov in zip(numbers, hoverable):
                    if pos in hov:
                        #dimmer.restore()
                        return int(number)
    
class Hoverable(object):
    """A rectangle that can be blitted in several states"""
    def __init__(self, pos, anchor = HAT_CENTERED, *states):
        """Inits the Hoverable. Takes 3 arguments:
            pos - where it should blit the state 0
            anchor - how should it position if redrawing
                    resizes
            states - the things needed to alternate between
            """
        self.x, self.y = pos
        self.drawn = None
        self.states = states
        #0 - left, 0.5 middle, 1 - right
        if anchor in (HAT_LEFT, HAT_LEFTDOWN, HAT_LEFTUP):
            self.xmult = 0
        elif anchor in (HAT_CENTERED, HAT_DOWN, HAT_UP):
            self.xmult = 0.5
        elif anchor in (HAT_RIGHT, HAT_RIGHTDOWN, HAT_RIGHTUP):
            self.xmult = 1
        #0 - up, 0.5 middle, 1 - down
        if anchor in (HAT_UP, HAT_LEFTUP, HAT_RIGHTUP):
            self.ymult = 0
        elif anchor in (HAT_CENTERED, HAT_LEFT, HAT_RIGHT):
            self.ymult = 0.5
        elif anchor in (HAT_DOWN, HAT_LEFTDOWN, HAT_RIGHTDOWN):
            self.ymult = 1
        
    def _measure(self, i):
        if i is None: i = 1
        j = self.states[0].get_rect()
        k = self.states[i].get_rect()
        width = k.w
        height = k.h
        dw = int((j.w - k.w) * self.xmult)
        dh = int((j.h - k.h) * self.ymult)
        return dw, dh, width, height
            
    def corners(self, i = None):
        """Returns the current four corners of the Hoverable:
    (topwidth, topheight, bottomwidth, bottomheight"""
        if i == None:
            i = self.drawn
        dw, dh, width, height = self._measure(i)
        return (self.x + dw,
                self.y + dh,
                self.x + width + dw,
                self.y + height + dh)

    def draw(self, i):
        """Draws state i.
            Todo: exception when i > len(states)
            """
        self.drawn = i
        x, y, _, _ = self.corners(i)
        pygame.display.get_surface().blit(self.states[i], (x,y))

    def __contains__(self, pos):
        """returns True if hovering over the currently drawn Hoverable"""
        x, y = pos
        x1,y1,x2,y2 = self.corners(self.drawn)
        return x1 < x < x2 and y1 < y < y2