import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Services.mapService import map_all_tiles, map_destroy

def eat():
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
            radius=0,
            shape="square",
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
                color=(80, 80, 80), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(50,150),
                size=random.randint(5,20),
                fadeSpeed=500,
            )
        
        if tile["isBomb"]:
            gainAmount = Global.playerStats["MaxHP"] / 5
            if Global.playerStats["HP"] + gainAmount <= Global.playerStats["MaxHP"]:
                Global.playerStats["HP"] += gainAmount
            else:
                Global.playerStats["HP"] = Global.playerStats["MaxHP"]

            text_label = TextLabel(
                text=f"+{gainAmount}HP",
                pos=tile["pos"],
                font_size=20,
                color=(0, 200, 0),
                font_name="Assets/Fonts/Minecraft.ttf",
                center=True,
            )
            text_label.moveTo(tile["pos"] - pygame.Vector2(0,50), speed=300)
            text_label.fadeOut(speed=300, onDone=text_label.kill)
            Global.uiGroup.add(text_label)
        else:
            gainAmount = Global.playerStats["MaxHP"] / 10
            Global.playerStats["HP"] -= gainAmount
            text_label = TextLabel(
                text=f"-{gainAmount}HP",
                pos=tile["pos"],
                font_size=20,
                color=(200, 0, 0),
                font_name="Assets/Fonts/Minecraft.ttf",
                center=True,
            )
            text_label.moveTo(tile["pos"] - pygame.Vector2(0,50), speed=300)
            text_label.fadeOut(speed=300, onDone=text_label.kill)
            Global.uiGroup.add(text_label)