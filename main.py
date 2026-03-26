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
from Services.mapService import create_map, handle_click, map_update
# mapPos = (
#     boxPos.x + (currSize.x - (cols * (tileSize[0] + offset) - offset)) / 2,
#     boxPos.y + (currSize.y - (rows * (tileSize[1] + offset) - offset)) / 2,
# )
currentMap = create_map(
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

# UI components
Global.uiGroup = pygame.sprite.Group()
from Utils.UiComponents.Box import Box
#minesweeperBox
currSize = pygame.Vector2(1100, 1000)
Global.minesweeperBox = Box(
    pos=pygame.Vector2(1350 - currSize.x/2,540 - currSize.y/2),
    size=currSize,
    groups=Global.uiGroup,
    color=(30, 30, 30, 0),
    border=True,
    borderColor=(50,50,50, 255),
    borderWidth=5,
    borderRadius=0,
)
Global.uiGroup.add(Global.minesweeperBox)
#mainGameBox
currSize = pygame.Vector2(750,600)
Global.mainGameBox = Box(
    pos=pygame.Vector2(400 - currSize.x/2,340 - currSize.y/2),
    size=currSize,
    groups=Global.uiGroup,
    color=(30, 30, 30, 0),
    border=True,
    borderColor=(50,50,50, 255),
    borderWidth=5,
    borderRadius=0,
)
Global.uiGroup.add(Global.mainGameBox)
#secondarySectionBox
currSize = pygame.Vector2(750,375)
Global.secondarySectionBox = Box(
    pos=pygame.Vector2(400 - currSize.x/2,850 - currSize.y/2),
    size=currSize,
    groups=Global.uiGroup,
    color=(30, 30, 30, 0),
    border=True,
    borderColor=(50,50,50, 255),
    borderWidth=5,
    borderRadius=0,
)
Global.uiGroup.add(Global.secondarySectionBox)

playerHPText = TextLabel(
    text=f"HP: {Global.playerHP} / {Global.playerMaxHP}",
    pos=pygame.Vector2(100,700),
    font_size=30,
    color=(0,200,0),
    font_name="Assets/Fonts/Rimouski.otf", 
    center=False,
)
playerMPText = TextLabel(
    text=f"MP: {Global.playerMP} / {Global.playerMaxMP}",
    pos=pygame.Vector2(100,725),
    font_size=30,
    color=(0,0,200),
    font_name="Assets/Fonts/Rimouski.otf",
    center=False,
)
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

from Services.mainGameService import mainGameService
Global.MainGameService = mainGameService()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        handle_click(currentMap, event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mouse_pos = pygame.mouse.get_pos()
                for tile in currentMap.tilesGroup:
                    if tile.rect.collidepoint(mouse_pos):
                        currentMap.mapDestroy(tile.index,4,"circle")
                        break
            if event.key == pygame.K_w:
                from Classes.Enemies.LaserEnemy import LaserEnemy
                newEnemy = LaserEnemy(
                    pos=pygame.Vector2(random.randint(450,650),random.randint(100,450)),
                    size=pygame.Vector2(200,200),
                    groups=Global.entityGroup,
                )
                Global.entityGroup.add(newEnemy)
                sortEntityGroup()
                
            if event.key == pygame.K_z:
                currentMap = create_map(
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
                from Classes.Enemies.SpikeEnemy import SpikeEnemy
                newEnemy = SpikeEnemy(
                    pos=pygame.Vector2(random.randint(450,650),random.randint(100,450)),
                    size=pygame.Vector2(200,200),
                    groups=Global.entityGroup,
                )
                Global.entityGroup.add(newEnemy)
                sortEntityGroup()
                
    screen.fill("white")
    map_update(currentMap)
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

    Global.uiGroup.update(screen)
    Global.uiGroup.draw(screen)
    
    playerHPText.setText(f"HP: {Global.playerHP} / {Global.playerMaxHP}")
    playerMPText.setText(f"MP: {Global.playerMP} / {Global.playerMaxMP}")
    Global.screen.blit(playerHPText.image, playerHPText.rect)
    Global.screen.blit(playerMPText.image, playerMPText.rect)

    pygame.display.flip()
    Global.dt = clock.tick(144) / 1000