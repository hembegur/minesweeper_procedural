import pygame, sys, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.ScrollBox import ScrollBox
from Utils.UiComponents.Shop import Shop
from Utils.UiComponents.Bar import Bar

class uiService:
    def __init__(self):
        super().__init__()
        self.shop = None
        #self.shop = Shop()
        #minesweeperBox
        self.hideBox : Box = None
        self.continueText : TextLabel = None
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
            pos=pygame.Vector2(50,700),
            font_size=30,
            color=(0,200,0),
            font_name="Assets/Fonts/Rimouski.otf", 
            center=False,
        )
        self.hpBar = Bar(
            pos=pygame.Vector2(250,715),
            size=pygame.Vector2(475, 10),
            groups=Global.uiGroup,
            value=100,
            maxValue=100,
            fillColor=(50, 200, 50, 255),
            emptyColor=(60, 60, 60, 255),
            border=False,
            smooth=True,
            smoothSpeed=150,
        )

        self.playerMPText = TextLabel(
            text=f"MP: {Global.playerStats["MP"]} / {Global.playerStats["MaxMP"]}",
            pos=pygame.Vector2(50,725),
            font_size=30,
            color=(0,0,200),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        self.mpBar = Bar(
            pos=pygame.Vector2(250,740),
            size=pygame.Vector2(475, 10),
            groups=Global.uiGroup,
            value=0,
            maxValue=100,
            fillColor=(60,225,225, 255),
            emptyColor=(60, 60, 60, 255),
            border=False,
            smooth=True,
            smoothSpeed=150,
        )

        self.playerUltText = TextLabel(
            text=f"ULT: {Global.playerStats["Ult"]} / {Global.playerStats["MaxUlt"]}",
            pos=pygame.Vector2(50,750),
            font_size=30,
            color=(200,0,200),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        self.ultBar = Bar(
            pos=pygame.Vector2(250,765),
            size=pygame.Vector2(475, 10),
            groups=Global.uiGroup,
            value=0,
            maxValue=100,
            fillColor=(200,0,200, 255),
            emptyColor=(60, 60, 60, 255),
            border=False,
            smooth=True,
            smoothSpeed=150,
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

        Global.toolBar = ScrollBox(
            pos=pygame.Vector2(163, 800),
            size=pygame.Vector2(475, 115),
            groups=Global.uiGroup,
            color=(220,220,220, 255),
            border=False,
            padding=5,
            spacing=15,
            direction="horizontal",
            scrollSpeed=20,
            scrollbar=False,
        )

    def spawnShop(self):
        self.shop = Shop()
        return self.shop

    def handleEvents(self, event):
        Global.inventoryBox.handleScroll(event)
        if self.shop:
            self.shop.handleEvent(event)

    def hideMap(self):
        if not self.hideBox or not self.continueText:
            currSize = pygame.Vector2(1100, 1000)
            self.hideBox = Box(
                pos=pygame.Vector2(1350 - currSize.x/2,540 - currSize.y/2),
                size=currSize,
                groups=Global.uiGroup,
                color=(30, 30, 30, 255),
                border=False,
            )
            Global.uiGroup.add(self.hideBox)
            self.continueText = TextLabel(
                text=f"Hover to continue",
                pos=pygame.Vector2(1350,540),
                font_size=80,
                color=(200,50,50),
                font_name="Assets/Fonts/Rimouski.otf",
                center=True,
            )
            Global.uiGroup.add(self.continueText)
    
    def revealMap(self):
        if self.hideBox or self.continueText:
            self.hideBox.kill()
            self.hideBox = None
            self.continueText.kill()
            self.continueText = None

    def update(self):
        self.playerHPText.setText(
            f"HP: {formatStat(Global.playerStats['HP'])} / {formatStat(Global.playerStats['MaxHP'])}"
        )

        self.playerMPText.setText(
            f"MP: {formatStat(Global.playerStats['MP'])} / {formatStat(Global.playerStats['MaxMP'])}"
        )

        self.playerUltText.setText(
            f"ULT: {formatStat(Global.playerStats['Ult'])} / {formatStat(Global.playerStats['MaxUlt'])}"
        )
        self.hpBar.setValue(Global.playerStats["HP"] / max(1, Global.playerStats["MaxHP"]) * 100)
        self.mpBar.setValue(Global.playerStats["MP"] / max(1, Global.playerStats["MaxMP"]) * 100)
        self.ultBar.setValue(Global.playerStats["Ult"] / max(1, Global.playerStats["MaxUlt"]) * 100)

        self.currentRoundText.setText(f"Current Round: {Global.currentRound}")
        self.moneyText.setText(f"$: {Global.money}")
        Global.screen.blit(self.playerHPText.image, self.playerHPText.rect)
        Global.screen.blit(self.playerMPText.image, self.playerMPText.rect)
        Global.screen.blit(self.playerUltText.image, self.playerUltText.rect)
        Global.screen.blit(self.currentRoundText.image, self.currentRoundText.rect)

def formatStat(value):
        return f"{value:.1f}".rstrip('0').rstrip('.')