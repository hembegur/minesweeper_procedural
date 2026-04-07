import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Services.mapService import map_all_tiles, map_destroy
from Utils.Game.mathStuff import Timer

def foresee():
    chosenTiles = []
    initialTile = None
    pos = None
    mouse = pygame.mouse.get_pos()
    for tile in map_all_tiles(Global.currentMap):
        if tile["rect"].collidepoint(mouse):
            pos = tile["rect"].center
            initialTile = tile["index"]
            break

    if pos:
        for tile in map_all_tiles(Global.currentMap):
            if initialTile.x + 2 >= tile["index"].x >= initialTile.x - 2 and initialTile.y + 2 >= tile["index"].y >= initialTile.y - 2:
                chosenTiles.append(tile)
        # map_destroy(
        #     m=Global.currentMap,
        #     initialPos=pygame.Vector2(chosenTile["index"].x, chosenTile["index"].y),
        #     radius=0,
        #     shape="square",
        # )
        randomChosen = []
        for _ in range(5):
            if len(chosenTiles) > 0:
                randomTile = random.choice(chosenTiles)
                randomChosen.append(randomTile)
                chosenTiles.remove(randomTile)
        boxOffset = pygame.Vector2(Global.minesweeperBox.rect.topleft)
        def spawnParticle(pos, color):
            particlePos = pos - boxOffset
            Particle(
                groups=Global.msParticleGroup,
                pos=particlePos,
                color=color,
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)),
                                        math.sin(random.uniform(0, 2 * math.pi))),
                speed=0,
                size=random.randint(30, 60),
                fadeSpeed=500,
            )
        def spawnParticles():
            for tile in randomChosen:
                particlePos = tile["pos"] - boxOffset
                Particle(
                    groups=Global.msParticleGroup,
                    pos=particlePos,
                    color=(175, 6, 204),
                    direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)),
                                            math.sin(random.uniform(0, 2 * math.pi))),
                    speed=0,
                    size=random.randint(30, 60),
                    fadeSpeed=500,
                )

        count = [0]
        def repeat():
            if count[0] >= 5:
                return
            
            if count[0] == 4:
                for tile in randomChosen:                    
                    if tile["isBomb"]:
                        chance = random.randint(1,100)
                        if chance <= 90:
                            spawnParticle(tile["pos"], (200,0,0))
                        else:
                            spawnParticle(tile["pos"], (0,200,0))
                    else:
                        chance = random.randint(1,100)
                        if chance <= 90:
                            spawnParticle(tile["pos"], (0,200,0))
                        else:
                            spawnParticle(tile["pos"], (200,0,0))
                return
            
            spawnParticles()
            count[0] += 1
            Timer(0.5, repeat, Global.timerGroup)

            

        repeat()
        
