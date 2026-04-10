import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Services.mapService import map_all_tiles, map_destroy

def nuke():
    chosenTile = None
    pos = None
    mouse = pygame.mouse.get_pos()
    for tile in map_all_tiles(Global.currentMap):
        if tile["rect"].collidepoint(mouse):
            pos = tile["rect"].center
            chosenTile = tile
            break
    if pos:
        map_destroy(
            m=Global.currentMap,
            initialPos=pygame.Vector2(chosenTile["index"].x, chosenTile["index"].y),
            radius=3,
            shape="square",
        )
        boxOffset = pygame.Vector2(Global.minesweeperBox.rect.topleft)
        for _ in range(40):
            particlePos = pygame.Vector2(
                pos[0] + random.randint(-20, 20),
                pos[1] + random.randint(-20, 20),
            ) - boxOffset 
            Particle(
                groups=Global.msParticleGroup, 
                pos=particlePos, 
                color=(50,50,50), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(200, 400),
                size=random.randint(100, 150),
                fadeSpeed=500,
            )