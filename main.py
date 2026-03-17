import pygame, sys, Global
pygame.init()
screen = pygame.display.set_mode((Global.screenWidth, Global.screenHeight), pygame.FULLSCREEN | pygame.SCALED)
Global.screen = screen
clock = pygame.time.Clock()

from Utils.Game.Hitbox import Hitbox
hitbox = Hitbox()
from Services.mapService import createMap
currentMap = createMap(
    cols=20,
    rows=15,
    offset=2,
    color=(100,100,100,255),
    hiddenColor=(50,50,50,255),
    revealColor=(200,200,200,255),
    bombColor=(255,50,50,255),
    flagColor=(220,220,0),
    mapPos=(800,150),
    tileSize=(50,50),
    bombCount=50
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        currentMap.handleClick(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mouse_pos = pygame.mouse.get_pos()
                for tile in currentMap.tilesGroup:
                    if tile.rect.collidepoint(mouse_pos):
                        currentMap.mapDestroy(tile.index,4,"circle")
                        break
            if event.key == pygame.K_w:
                mouse_pos = pygame.mouse.get_pos()
                for tile in currentMap.tilesGroup:
                    if tile.rect.collidepoint(mouse_pos):
                        currentMap.mapHidden(tile.index,4,"circle")
                        break
            if event.key == pygame.K_z:
                currentMap = createMap(
                    cols=20,
                    rows=15,
                    offset=2,
                    color=(100,100,100,255),
                    hiddenColor=(50,50,50,255),
                    revealColor=(200,200,200,255),
                    bombColor=(255,50,50,255),
                    flagColor=(220,220,0),
                    mapPos=(800,150),
                    tileSize=(50,50),
                    bombCount=50
                )
            if event.key == pygame.K_e:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                def hit():
                    print("nigger")
                newHB = hitbox.new(
                    pos=mouse_pos,
                    visualize=True,
                    size=pygame.Vector2(100,100),
                    lifetime=3,
                    hitFunction=hit,
                )

    screen.fill("white")

    currentMap.update()
    hitbox.update()

    pygame.display.flip()
    Global.dt = clock.tick(144) / 1000