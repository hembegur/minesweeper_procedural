import pygame, sys, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.ScrollBox import ScrollBox

class uiService:
    def __init__(self):
        super().__init__()
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

        self.playerHPText = TextLabel(
            text=f"HP: {Global.playerHP} / {Global.playerMaxHP}",
            pos=pygame.Vector2(100,700),
            font_size=30,
            color=(0,200,0),
            font_name="Assets/Fonts/Rimouski.otf", 
            center=False,
        )
        self.playerMPText = TextLabel(
            text=f"MP: {Global.playerMP} / {Global.playerMaxMP}",
            pos=pygame.Vector2(100,725),
            font_size=30,
            color=(0,0,200),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )

        self.playerUltText = TextLabel(
            text=f"ULT: {Global.playerUlt} / {Global.playerMaxUlt}",
            pos=pygame.Vector2(100,750),
            font_size=30,
            color=(200,0,200),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )

        self.currentRoundText = TextLabel(
            text=f"Current Round: {Global.currentRound}",
            pos=pygame.Vector2(50,5),
            font_size=30,
            color=(20,20,20),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )

        self.Inventory = ScrollBox(
            pos=pygame.Vector2(50, 925),
            size=pygame.Vector2(700, 100),
            groups=Global.uiGroup,
            color=(220,220,220, 255),
            border=False,
            padding=10,
            spacing=6,
            direction="horizontal",
            scrollSpeed=20,
            scrollbar=True,
            scrollbarColor=(120, 120, 120, 255),
            scrollbarWidth=6,
        )
        label = TextLabel("TEST_TEST", (0, 0), font_size=24, color=(0,0,0))
        self.Inventory.addItem(label.image)
        for _ in range(20):
            icon = pygame.Surface((280, 60), pygame.SRCALPHA)
            icon.fill((0,0,0, 200))
            self.Inventory.addItem(icon)

    def handleEvents(self, event):
        self.Inventory.handleScroll(event)

    def update(self):
        self.playerHPText.setText(f"HP: {Global.playerHP} / {Global.playerMaxHP}")
        self.playerMPText.setText(f"MP: {Global.playerMP} / {Global.playerMaxMP}")
        self.playerUltText.setText(f"ULT: {Global.playerUlt} / {Global.playerMaxUlt}")
        self.currentRoundText.setText(f"Current Round: {Global.currentRound}")
        Global.screen.blit(self.playerHPText.image, self.playerHPText.rect)
        Global.screen.blit(self.playerMPText.image, self.playerMPText.rect)
        Global.screen.blit(self.playerUltText.image, self.playerUltText.rect)
        Global.screen.blit(self.currentRoundText.image, self.currentRoundText.rect)
