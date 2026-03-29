import pygame, Global
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.Button import Button
from Classes.Items.Items import itemLoader, SimpleItem

class SimpleImage(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        imagePath: str = None,
        layer: int = 10,
    ):
        super().__init__()
        groups.add(self, layer = layer)
        self.pos  = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.image = Global.loadImage(imagePath, (int(size.x), int(size.y)))
        self.rect = self.image.get_rect(center=self.pos)

class buySlot:
    def __init__(self, pos, buttonGroup, itemData=None):
        self.pos = pos
        self.itemClass : SimpleItem = None
        self.bought = False
        self.itemImage = None

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

        self.priceText = TextLabel(
            text="None",
            pos=pos + pygame.Vector2(self.itemFrame.size.x/2, 175),
            font_size=25,
            color=(50,150,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(self.priceText)

        def onClickPlaceHolder():
            pass
        self.onClickFunc = onClickPlaceHolder

        if itemData:
            self.itemImage = SimpleImage(
                pos = pos + pygame.Vector2(self.itemFrame.size.x/2, self.itemFrame.size.y/2),
                size=pygame.Vector2(125,125),
                groups=Global.uiGroup,
                imagePath=itemData["ImagePath"],
            )
            self.priceText.setText(f"${str(itemData["Price"])}")

            def onClick():
                if float(itemData["Price"]) <= Global.money and not self.bought:
                    Global.money -= itemData["Price"]
                    self.itemClass = itemData["Link"]()
                    Global.inventoryBox.addItem(self.itemClass)

                    self.itemImage.kill()
                    self.priceText.setText(f"None")
                    self.bought = True
            self.onClickFunc = onClick

        self.buyButton, self.buyButtonText = buttonAndText(
            pos=pos + pygame.Vector2(0, 200),
            size=pygame.Vector2(150, 50),
            group=buttonGroup,
            color=(253, 255, 158, 255),
            hoverColor=(137, 138, 85, 255),
            clickColor=(68, 69, 43, 255),
            text="Buy",
            onClick=self.onClickFunc,
        )
    def destroy(self):
        self.buyButton.kill()
        self.priceText.kill()
        self.itemFrame.kill()
        self.buyButtonText.kill()
        if self.itemImage:
            self.itemImage.kill()    

def buttonAndText(
    pos,
    size,
    color,
    hoverColor,
    clickColor,
    onClick,
    text,
    group,
):
    buyButton = Button(
        pos=pos,
        size=size,
        groups=Global.uiGroup,
        color=color,
        hoverColor=hoverColor,
        clickColor=clickColor,
        border=True,
        borderWidth=5,
        borderColor=(50, 50, 50, 255),
        borderRadius=15,
        onClick=onClick,
    )
    group.add(buyButton)

    t = TextLabel(
        text=text,
        pos=pos + pygame.Vector2(buyButton.size.x/2, buyButton.size.y/2),
        font_size=25,
        color=(50,50,50),
        font_name="Assets/Fonts/Rimouski.otf",
        center=True,
    )
    Global.uiGroup.add(t)

    return buyButton, t

class Shop:
    def __init__(
            self, 
            pos = pygame.Vector2(950,85),
        ):
        self.pos = pos
        self.buttonGroup = pygame.sprite.Group()
        self.itemsLoader = itemLoader()
        self.tools = {}
        self.items = self.itemsLoader.randomItems(3)
        self.rerollPrice = 20
        self.buySlots = []
        self.removed = False

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

        self.labels = []
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
        self.labels.append(t)

        t = TextLabel(
            text=f"Tools for sale:",
            pos=pos + pygame.Vector2(35,100),
            font_size=30,
            color=textColor,
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(t)
        self.labels.append(t)

        t = TextLabel(
            text=f"Items for sale:",
            pos=pos + pygame.Vector2(35,425),
            font_size=30,
            color=textColor,
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(t)
        self.labels.append(t)
        
        def spawnBuySlots():
            for buyslot in self.buySlots:
                buyslot.destroy()
            placePos = pygame.Vector2(125,160)
            for i in range(3):
                newBuySlot = buySlot(
                    pos=pos + placePos + pygame.Vector2(200 * i,0),
                    buttonGroup=self.buttonGroup,
                )
                self.buySlots.append(newBuySlot)
            placePos = pygame.Vector2(125,480)
            for i in range(3):
                newBuySlot = buySlot(
                    pos=pos + placePos + pygame.Vector2(200 * i,0),
                    buttonGroup=self.buttonGroup,
                    itemData=self.items[i],
                )
                self.buySlots.append(newBuySlot)
        spawnBuySlots()

        def reroll():
            if Global.money >= self.rerollPrice:
                spawnBuySlots()
                Global.money -= self.rerollPrice
                self.rerollPrice += 50
                self.items = self.itemsLoader.randomItems(3)
                self.rerollButtonText.setText(f"Reroll({self.rerollPrice})")
        self.rerollButton, self.rerollButtonText = buttonAndText(
            pos=pos + pygame.Vector2(125,775),
            size=pygame.Vector2(200, 50),
            group=self.buttonGroup,
            color=(209, 73, 82, 255),
            hoverColor=(191, 27, 38, 255),
            clickColor=(112, 17, 23, 255),
            onClick=reroll,
            text=f"Reroll({self.rerollPrice})",
        )

        #next wave button
        def nextWave():
            self.removeShop()
        self.nextWaveButton, self.nextWaveButtonText = buttonAndText(
            pos=pos + pygame.Vector2(375,775),
            size=pygame.Vector2(200, 50),
            group=self.buttonGroup,
            color=(79, 210, 214, 255),
            hoverColor=(71, 188, 191, 255),
            clickColor=(56, 141, 143, 255),
            onClick=nextWave,
            text="Next wave!",
        )
        
    def handleEvent(self, event):
        for button in self.buttonGroup:
            button.handleEvent(event)

    def removeShop(self):
        self.removed = True
        for buyslot in self.buySlots:
            buyslot.destroy()
        self.buySlots.clear()

        for label in self.labels:
            label.kill()
        self.labels.clear()

        self.buttonGroup.empty()
        self.mainFrame.kill()
        self.rerollButton.kill()
        self.rerollButtonText.kill()
        self.nextWaveButton.kill()
        self.nextWaveButtonText.kill()