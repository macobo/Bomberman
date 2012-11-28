# -*- coding: utf-8 -*-

import Objects
import random

def tryPlace(map, obj):
    (x, y) = random.randrange(map.size), random.randrange(map.size)
    for player in map. players:
        pxy = player.getRoundCoordinate()
        if (x,y) in neighbors(pxy, map.size) or (x,y) == pxy:
            return False
    here = map.objectsAt((x,y))
    if obj.collectable:
        canPlace = (bool(here) and all(x.fragile for x in here))
    else:
        canPlace = len(here) == 0
        canPlace = canPlace or all(obj.canGoUnder(x) for x in here)
        canPlace = canPlace and (not obj.collectable or (bool(here) and all(x.fragile for x in here)))
    if canPlace:
        map.add(obj, (x,y))
        return True
    return False

def mapGenerator(map, size):
    iteration = 0
    while True:
        iteration += 1
        map.resetMap()
        for obj in Objects.placeable:
            placed = 0
            amount = obj.amount(map.size)
            while placed < amount:
                if tryPlace(map, obj):
                    placed += 1
        if validConfiguration(map, size, map.players):
            break
    #print iteration
                
def neighbors(xy, size):
    x, y = xy
    for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < size and 0 <= ny < size:
            yield nx, ny
                
def validConfiguration(map, size, players):
    # check if there's room around the player
#    for player in players:
#        x, y = player.getRoundCoordinate()
#        for dx, dy in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:
#            nx, ny = x+dx, y+dy
#            if 0 <= nx < size and 0 <= ny < size and map.objectsAt((nx,ny)):
#                print ":("
#                return False
    # check if we can go from one corner to another
    from collections import deque
    visited = set()
    Q = deque([players[0].getRoundCoordinate()])
    while len(Q) and any(player.getRoundCoordinate() not in visited for player in players):
        xy = Q.popleft()
        canGo = xy not in visited
        canGo = canGo and not any(x.solid and not x.fragile for x in map.objectsAt(xy))
        if canGo:
            visited.add(xy)
            for nxy in neighbors(xy, size):
                Q.append(nxy)
    return all(player.getRoundCoordinate() in visited for player in players)