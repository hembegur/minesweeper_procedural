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

from Utils.Game.SoundManager import soundManager
SoundManager = soundManager()

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

from Data.Default import DefaultData
defaultData = DefaultData()
money = 000000000000
playerStats = defaultData.playerStats.copy()
playerStatsMultiplier = defaultData.playerStatsMultiplier.copy()
playerStatsGain = defaultData.playerStatsGain.copy()
playerStatsLose = defaultData.playerStatsLose.copy()
enemyStats = defaultData.enemyStats.copy()
rarityColor = defaultData.rarityColor.copy()
difficultyScale = defaultData.difficultyScale.copy()
def getEnemyStats(enemyName: str) -> dict:
    base   = defaultData.enemyStats[enemyName].copy()
    round  = max(0, currentRound - 1)  # round 1 = no scaling
    scale  = difficultyScale
    stats  = base.copy()

    if "HP" in stats:
        stats["HP"] = int(base["HP"] * (1 + scale[currentDifficulty]["HPScale"] * round))
    if "Money" in stats:
        stats["Money"] = int(base["Money"] * (1 + scale[currentDifficulty]["MoneyScale"] * round))
    for key in stats:
        if "Damage" in key:
            stats[key] = int(base[key] * (1 + scale[currentDifficulty]["DamageScale"] * round))

    return stats

currentRarity = defaultData.startRarity
def updateRarity(roundNum, maxRounds=20):
    t = roundNum / maxRounds  # 0 → 1
    current = {}
    for k in defaultData.targetRarity:
        current[k] = int(defaultData.startRarity[k] + (defaultData.targetRarity[k] - defaultData.startRarity[k]) * t)
    return current

currentRound = 20
currentDifficulty = "Normal"
gameState = "Preparing"
enemyCount = 0

from Services.mapService import create_map
currentMap : create_map = None

gameProgress = defaultData.gameProgress.copy()

from Data.Data import SaveManager
saveManager = SaveManager()