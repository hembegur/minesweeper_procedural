import pygame, sys, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.ScrollBox import ScrollBox
from Utils.UiComponents.Shop import Shop

class uiService:
    def __init__(self):
        super().__init__()
        self.shop = None
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
            text=f"HP: {Global.playerStats["HP"]} / {Global.playerStats["MaxHP"]}",
            pos=pygame.Vector2(100,700),
            font_size=30,
            color=(0,200,0),
            font_name="Assets/Fonts/Rimouski.otf", 
            center=False,
        )
        self.playerMPText = TextLabel(
            text=f"MP: {Global.playerStats["MP"]} / {Global.playerStats["MaxMP"]}",
            pos=pygame.Vector2(100,725),
            font_size=30,
            color=(0,0,200),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )

        self.playerUltText = TextLabel(
            text=f"ULT: {Global.playerStats["Ult"]} / {Global.playerStats["MaxUlt"]}",
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

        self.moneyText = TextLabel(
            text=f"$: {Global.money}",
            pos=pygame.Vector2(450,5),
            font_size=30,
            color=(50,200,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(self.moneyText)

        Global.inventoryBox = ScrollBox(
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
            scrollbarWidth=3,
        )

    def spawnShop(self):
        self.shop = Shop()
        return self.shop

    def handleEvents(self, event):
        Global.inventoryBox.handleScroll(event)
        if self.shop:
            self.shop.handleEvent(event)

    def update(self):
        self.playerHPText.setText(f"HP: {Global.playerStats["HP"]} / {Global.playerStats["MaxHP"]}")
        self.playerMPText.setText(f"MP: {Global.playerStats["MP"]} / {Global.playerStats["MaxMP"]}")
        self.playerUltText.setText(f"ULT: {Global.playerStats["Ult"]} / {Global.playerStats["MaxUlt"]}")
        self.currentRoundText.setText(f"Current Round: {Global.currentRound}")
        self.moneyText.setText(f"$: {Global.money}")
        Global.screen.blit(self.playerHPText.image, self.playerHPText.rect)
        Global.screen.blit(self.playerMPText.image, self.playerMPText.rect)
        Global.screen.blit(self.playerUltText.image, self.playerUltText.rect)
        Global.screen.blit(self.currentRoundText.image, self.currentRoundText.rect)
