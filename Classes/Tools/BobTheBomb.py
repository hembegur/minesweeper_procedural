import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Services.mapService import map_all_tiles, map_destroy

def bob_the_bomb():
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
            radius=1,
            shape="circle",
        )
        boxOffset = pygame.Vector2(Global.minesweeperBox.rect.topleft)
        for _ in range(20):
            particlePos = pygame.Vector2(
                pos[0] + random.randint(-20, 20),
                pos[1] + random.randint(-20, 20),
            ) - boxOffset 
            Particle(
                groups=Global.msParticleGroup, 
                pos=particlePos, 
                color=(255, 200, 3), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(100, 250),
                size=random.randint(50, 90),
                fadeSpeed=500,
            )