import pygame, sys, Global, random
pygame.init()
screen = pygame.display.set_mode((Global.screenWidth, Global.screenHeight), pygame.FULLSCREEN | pygame.SCALED)
Global.screen = screen
clock = pygame.time.Clock()

from Classes.Attacks.Spike import spawnSpike
from Utils.Game.Hitbox import Hitbox
hitbox = Hitbox()
Global.hitbox = hitbox
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
    mapPos=(857,150),
    tileSize=(50,50),
    bombCount=50
)

minesweeperSurface = pygame.Surface(Global.minesweeperSurfaceSize, pygame.SRCALPHA)
minesweeperRect = minesweeperSurface.get_rect()
minesweeperRect.center = pygame.Vector2(1350,540)
Global.minesweeperSurface = minesweeperSurface
Global.minesweeperRect = minesweeperRect

mouseHB = hitbox.new(
    pos=pygame.Vector2(0,0),
    visualize=True,
    size=pygame.Vector2(25,25),
    lifetime=None,
    hitFunction=None,
    owner=pygame.mouse,
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
                    mapPos=(857,150),
                    tileSize=(50,50),
                    bombCount=50
                )
            if event.key == pygame.K_e:
                spawnSpike()
                

    mouseHB.position = pygame.Vector2(pygame.mouse.get_pos())
    screen.fill("white")
   
    currentMap.update()
    hitbox.update(screen)
    screen.blit(minesweeperSurface, minesweeperRect)
    minesweeperSurface.fill((200, 200, 200, 0))
    Global.attackGroup.update()
    Global.attackGroup.draw(minesweeperSurface)
    Global.particleGroup.update(Global.dt)
    Global.particleGroup.draw(minesweeperSurface)
    
    

    pygame.display.flip()
    Global.dt = clock.tick(60) / 1000