import pygame

screenWidth = 1920 #1280 #1920
screenHeight = 1080 #720#1080
dt = 0
screen : pygame.display.set_mode = None
animationFPS = 12
animationCache = {}

minesweeperSurface : pygame.Surface = None
minesweeperRect : pygame.Rect = None
minesweeperSurfaceSize = pygame.Vector2(1100, 1000)

attackGroup : pygame.sprite.Group = pygame.sprite.Group()
particleGroup : pygame.sprite.Group = pygame.sprite.Group()

from Utils.Game.Hitbox import Hitbox
hitbox : Hitbox = None
