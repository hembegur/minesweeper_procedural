import pygame, sys, Global, random
pygame.init()
screen = pygame.display.set_mode((Global.screenWidth, Global.screenHeight), pygame.FULLSCREEN | pygame.SCALED)
Global.screen = screen
clock = pygame.time.Clock()
Global.dt = clock.tick(144) / 1000

from Utils.UiComponents.TextLabel import TextLabel
from Utils.Game.Hitbox import Hitbox
hitbox = Hitbox()
Global.hitbox = hitbox
from Services.mapService import handle_click, mapLock, mapUnLock, map_all_tiles

# UI components
from Utils.UiComponents.Box import Box


#----------------------------------------------------
from Classes.Player import PlayerSprite

player = PlayerSprite(
    pos=pygame.Vector2(180,350),
    size=pygame.Vector2(300,300),
    groups=Global.entityGroup,
)
Global.entityGroup.add(player, layer=-999)
Global.playerSprite = player


mouseHB = hitbox.new(
    pos=pygame.Vector2(pygame.mouse.get_pos()),
    visualize=True,
    size=pygame.Vector2(25,25),
    lifetime=None,
    hitFunction=None,
    owner=pygame.mouse,
)

def sortEntityGroup():
    for entity in Global.entityGroup:
        if entity is Global.playerSprite:
            continue
        Global.entityGroup.change_layer(entity, entity.rect.bottom)

from Services.uiService import uiService
Global.UiService = uiService()
from Services.mainGameService import mainGameService
Global.MainGameService = mainGameService()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_click(Global.currentMap, event)
        Global.UiService.handleEvents(event=event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                from Classes.Attacks.SpikePunch import spawnSpikePunch
                spawnSpikePunch(damage=15)
            if event.key == pygame.K_a:
                pass
            if event.key == pygame.K_w:
                from Classes.Enemies.LaserEnemy import LaserEnemy
                newEnemy = LaserEnemy(
                    pos=pygame.Vector2(random.randint(450,650),random.randint(100,450)),
                    size=pygame.Vector2(200,200),
                    groups=Global.entityGroup,
                )
                Global.entityGroup.add(newEnemy)
                sortEntityGroup()
            if event.key == pygame.K_e:
                from Classes.Enemies.SpikeEnemy import SpikeEnemy
                newEnemy = SpikeEnemy(
                    pos=pygame.Vector2(random.randint(450,650),random.randint(100,450)),
                    size=pygame.Vector2(200,200),
                    groups=Global.entityGroup,
                )
                Global.entityGroup.add(newEnemy)
                sortEntityGroup()
                
    screen.fill("white")
    mouseHB.pos = pygame.Vector2(pygame.mouse.get_pos())
    hitbox.update(screen)

    Global.minesweeperBox.canvas.fill((0, 0, 0, 0))
    Global.mainGameBox.canvas.fill((0, 0, 0, 0))
    Global.secondarySectionBox.canvas.fill((0, 0, 0, 0))

    Global.msAttackGroup.update()
    Global.msAttackGroup.draw(Global.minesweeperBox.canvas)
    Global.msParticleGroup.update()
    Global.msParticleGroup.draw(Global.minesweeperBox.canvas)

    Global.mainBackGroundGroup.update()
    Global.mainBackGroundGroup.draw(Global.mainGameBox.canvas)
    Global.entityGroup.update()
    Global.entityGroup.draw(Global.mainGameBox.canvas)
    Global.mainAttackGroup.update()
    Global.mainAttackGroup.draw(Global.mainGameBox.canvas)

    Global.MainGameService.update()
    Global.UiService.update()

    Global.uiGroup.update(screen)
    Global.uiGroup.draw(screen)

    Global.timerGroup.update()

    pygame.display.flip()
    Global.dt = clock.tick(144) / 1000