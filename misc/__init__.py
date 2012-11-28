# -*- coding: utf-8 -*-
from pygame.locals import *
from os.path import join
NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)
DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
P2_KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RCTRL]
P1_KEYS = [K_w, K_s, K_a, K_d, K_LCTRL]

HAPPY, NORMAL, SAD = 2,1,0

URMASPICS = {
    HAPPY: join("resources","images","faces","urmas.happy.jpg"),
    NORMAL: join("resources","images","faces","urmas.normal.jpg"),
    SAD: join("resources","images","faces","urmas.sad.jpg"),
}

KATRINPICS = {
    HAPPY: join("resources","images","faces","katrin.happy.jpg"),
    NORMAL: join("resources","images","faces","katrin.normal.jpg"),
    SAD: join("resources","images","faces","katrin.sad.jpg"),
}

fontPath = join("resources", "fonts", "Jokerman.ttf")
titleImagePath = join("resources", "images", "title.jpg")

COMMENTS = [
    "Pihtas, põhjas",
    "Tere hommikust!",
    "Mis loed seal\najalehte?",
    "Mis magad seal?"
]

SUICIDECOMMENTS = [
    "Oih!",
    "See veel puudus",
    "Nojah siis"
]