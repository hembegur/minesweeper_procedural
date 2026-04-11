import pygame

tick = 0
dt = 0
mainBackGroundDt = 0
speedupMultiplier = 1

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
mainAttackGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
entityGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
mainBackGroundGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
uiGroup : pygame.sprite.Group = pygame.sprite.LayeredUpdates()
timerGroup : pygame.sprite.Group = pygame.sprite.Group()

from Classes.Player import PlayerSprite
playerSprite : PlayerSprite = None

from Utils.Game.Hitbox import Hitbox
hitbox : Hitbox = None

from Utils.UiComponents.ScrollBox import ScrollBox
inventoryBox: ScrollBox = None
toolBar: ScrollBox = None

money = 1000000000000
currentRarity = {
    "Common" : 30,
    "Rare" : 30,
    "Epic" : 30,
}
playerStats = {
    "HP" :  100,
    "MP" :  0,
    "Ult" : 0,
    "MaxHP" : 100,
    "MaxMP" : 10,
    "MaxUlt" : 1,
    "NormalDamage" : 10,
    "BaseAttackSpeed" : 250,
    "AttackSpeed": 100,
    "Burst" : 3,
    "BurstAttackSpeed": 800,
    "HPRegen" : 0,
    "Defense" : 0,
    "LifeSteal" : 0,
    "Aoe" : 0,
}
playerStatsMultiplier = {
    "NormalDamage" : 100,
    "UltDamage" : 100,
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
        "HP" : 30,
        "Damage" : 10,
        "CD": 4
    },
    "LaserEnemy" : {
        "HP" : 25,
        "Damage" : 10,
        "CD": 4
    },
    "ClownEnemy" : {
        "HP" : 40,
        "PunchDamage" : 10,
        "SpikeDamage" : 5,
        "CD": 4,
    },
    "MinigunEnemy" : {
        "HP" : 25,
        "Damage" : 8,
        "CD": 6,
        "BulletCount": 30,
    },
    "Monki" : { #BOSS
        "HP" : 1000,
        "CD": 6,
    }
}

rarityColor = {
    "Common" : { 
        "color" : (250, 250, 250, 255), 
        "borderColor" : (50, 50, 50, 255) 
    },
    "Rare": {
        "color": (180, 210, 255, 255),
        "borderColor": (0, 100, 255, 255)
    },
    "Epic": {
        "color": (220, 180, 255, 255),
        "borderColor": (180, 0, 255, 255)
    }
}

currentRound = 20
currentDifficulty = "Normal"
gameState = "Preparing"
enemyCount = 0

from Services.mapService import create_map
currentMap : create_map = None

gameProgress = {
    "Normal": {
        "SpawnRate": (1,2),
        "Round1" : {
            # "SpikeEnemy" : {
            #     "EnemyLeft" : 1,
            #     "MaxEnemy": 1,
            # },
            "ClownEnemy" : {
                "EnemyLeft" : 10,
                "MaxEnemy": 10,
            },
        },
        "Round2" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 1,
                "MaxEnemy": 1
            },
        },
        "Round3" : {
            "SpikeEnemy" : {
                "EnemyLeft" : 1,
                "MaxEnemy": 1
            },
            "LaserEnemy" : {
                "EnemyLeft" : 1,
                "MaxEnemy": 1
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
        "Round20" : {
            "Monki" : {
                "EnemyLeft" : 1,
                "MaxEnemy": 1
            },
        }
    }
}