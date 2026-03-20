import pygame

screenWidth = 1920 #1280 #1920
screenHeight = 1080 #720#1080
dt = 0
screen : pygame.display.set_mode = None
animationFPS = 12
animationCache = {}

from Utils.UiComponents.Box import Box
minesweeperBox: Box = None
minesweeperSurfaceSize = pygame.Vector2(1100, 1000)
mainGameBox: Box = None
secondarySectionBox: Box = None

attackGroup : pygame.sprite.Group = pygame.sprite.Group()
particleGroup : pygame.sprite.Group = pygame.sprite.Group()

from Utils.Game.Hitbox import Hitbox
hitbox : Hitbox = None

playerHP : int = 100
playerMP : int = 0
playerMaxHP : int = 100
playerMaxMP : int = 10
