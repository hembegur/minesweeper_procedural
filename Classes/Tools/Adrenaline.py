import pygame, Global
from Utils.Game.mathStuff import Timer
from Utils.UiComponents.Box import Box

def adrenaline():
    Global.speedupMultiplier = 0.4
    Global.playerStatsGain["MP"] *= 2

    currSize = pygame.Vector2(2000,2000)
    screenEffect = Box(
        pos=pygame.Vector2(0,0),
        size=currSize,
        groups=Global.uiGroup,
        color=(0, 0, 200, 100),
        border=True,
        borderColor=(50,50,50, 255),
        borderWidth=5,
        borderRadius=0,
    )
    Global.uiGroup.add(screenEffect)

    def onend():
        Global.speedupMultiplier = 1
        Global.playerStatsGain["MP"] /= 2
        screenEffect.kill()

    Timer(8, onend, Global.timerGroup)