import pygame, Global
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.Button import Button

class buySlot:
    def __init__(self, pos):
        self.pos = pos

        self.itemFrame = Box(
            pos=pos,
            size=pygame.Vector2(150, 150),
            groups=Global.uiGroup,
            color=(250, 250, 250, 255),
            border=True,
            borderColor=(50, 50, 50, 255),
            borderWidth=5,
            borderRadius=0,
        )
        Global.uiGroup.add(self.itemFrame)

        self.buyButton = Button(
            pos=pos + pygame.Vector2(0, 175),
            size=pygame.Vector2(150, 50),
            groups=Global.uiGroup,
            color=(253, 255, 158, 255),
            hoverColor=(137, 138, 85, 255),
            clickColor=(68, 69, 43, 255),
            border=True,
            borderWidth=5,
            borderColor=(50, 50, 50, 255),
            borderRadius=15,
            onClick=lambda: print("clicked!"),
        )

        t = TextLabel(
            text=f"Buy",
            pos=pos + pygame.Vector2(0, 175) + pygame.Vector2(75, 25),
            font_size=25,
            color=(50,50,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(t)


class Shop:
    def __init__(
            self, 
            pos = pygame.Vector2(950,85),
        ):
        self.pos = pos
        self.tools = {}
        self.items = {}

        self.mainFrame = Box(
            pos=pos,
            size=pygame.Vector2(800,900),
            groups=Global.uiGroup,
            color=(230, 230, 230, 255),
            border=True,
            borderColor=(50, 50, 50, 255),
            borderWidth=5,
            borderRadius=0,
        )
        Global.uiGroup.add(self.mainFrame)

        textColor = (50,50,50)
        t = TextLabel(
            text=f"Cool Shop :3",
            pos=pos + pygame.Vector2(400,50),
            font_size=50,
            color=textColor,
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(t)

        t = TextLabel(
            text=f"Tools for sale:",
            pos=pos + pygame.Vector2(35,100),
            font_size=30,
            color=textColor,
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(t)
        placePos = pygame.Vector2(125,160)
        for i in range(3):
            newBuySlot = buySlot(
                pos=pos + placePos + pygame.Vector2(200 * i,0),
            )

        t = TextLabel(
            text=f"Items for sale:",
            pos=pos + pygame.Vector2(35,425),
            font_size=30,
            color=textColor,
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(t)
        placePos = pygame.Vector2(125,480)
        for i in range(3):
            newBuySlot = buySlot(
                pos=pos + placePos + pygame.Vector2(200 * i,0),
            )

        self.rerollButton = Button(
            pos=pos + pygame.Vector2(125,775),
            size=pygame.Vector2(200, 50),
            groups=Global.uiGroup,
            color=(209, 73, 82, 255),
            hoverColor=(191, 27, 38, 255),
            clickColor=(112, 17, 23, 255),
            border=True,
            borderWidth=5,
            borderColor=(50, 50, 50, 255),
            borderRadius=15,
            onClick=lambda: print("clicked!"),
        )
        t = TextLabel(
            text=f"Reroll - 67",
            pos=pos + pygame.Vector2(125,775) + pygame.Vector2(100, 25),
            font_size=25,
            color=(50,50,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(t)

        #next wave button
        self.nextWaveButton = Button(
            pos=pos + pygame.Vector2(375,775),
            size=pygame.Vector2(200, 50),
            groups=Global.uiGroup,
            color=(79, 210, 214, 255),
            hoverColor=(71, 188, 191, 255),
            clickColor=(56, 141, 143, 255),
            border=True,
            borderWidth=5,
            borderColor=(50, 50, 50, 255),
            borderRadius=15,
            onClick=lambda: print("clicked!"),
        )
        t = TextLabel(
            text=f"Next wave!",
            pos=pos + pygame.Vector2(375,775) + pygame.Vector2(100, 25),
            font_size=25,
            color=(50,50,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(t)
        

    def removeShop(self):
        pass