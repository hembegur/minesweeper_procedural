import pygame

dt = 0
mainBackGroundDt = 0

screenWidth = 1920 #1280 #1920
screenHeight = 1080 #720#1080
screen : pygame.display.set_mode = None
animationFPS = 12
animationCache = {}
cachedImages = {}
def loadImage(path: str, size: tuple = None):
    key = (path, size)
    if key not in cachedImages:
        img = pygame.image.load(path).convert_alpha()
        cachedImages[key] = pygame.transform.scale(img, size) if size else img
    return cachedImages[key]

from Services.mainGameService import mainGameService
MainGameService: mainGameService = None
from Services.uiService import uiService
UiService : uiService = None

from Utils.UiComponents.Box import Box
minesweeperBox: Box = None
minesweeperSurfaceSize = pygame.Vector2(1100, 1000)
mainGameBox: Box = None
secondarySectionBox: Box = None

msAttackGroup : pygame.sprite.Group = pygame.sprite.Group()
msParticleGroup : pygame.sprite.Group = pygame.sprite.Group()
mainAttackGroup : pygame.sprite.Group = pygame.sprite.Group()
entityGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
mainBackGroundGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
uiGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()

from Classes.Player import PlayerSprite
playerSprite : PlayerSprite = None

from Utils.Game.Hitbox import Hitbox
hitbox : Hitbox = None

from Utils.UiComponents.ScrollBox import ScrollBox
inventoryBox: ScrollBox = None
money = 10000
playerStats = {
    "HP" :  100,
    "MP" :  0,
    "Ult" : 0,
    "MaxHP" : 100,
    "MaxMP" : 100,
    "MaxUlt" : 1,
    "NormalDamage" : 10,
    "UltDamage" : 30,
    "NormalCD": 2.5,
}

playerStatsGain = {
    "HP" :  1,
    "MP" :  1,
    "Ult" : 1,
}

playerStatsLose = {
    "HP" :  1,
    "MP" :  1,
    "Ult" : 1,
}

enemyStats = {
    "SpikeEnemy" : {
        "Damage" : 10,
        "CD": 4
    },
    "LaserEnemy" : {
        "Damage" : 10,
        "CD": 4
    }
}


currentRound = 1
currentDifficulty = "Normal"
gameState = "Preparing"
enemyCount = 0

from Services.mapService import create_map
currentMap : create_map = None

gameProgress = {
    "Normal": {
        "SpawnRate": (1,2),
        "Round1" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 1,
                "MaxEnemy": 1,
            },
        },
        "Round2" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 12,
                "MaxEnemy": 6
            },
        },
        "Round3" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 9,
                "MaxEnemy": 3
            },
            "LaserEnemy" : {
                "EnemyLeft" : 9,
                "MaxEnemy": 3
            },
        },
        "Round4" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 15,
                "MaxEnemy": 5
            },
            "LaserEnemy" : {
                "EnemyLeft" : 15,
                "MaxEnemy": 5
            },
        },
    }
}