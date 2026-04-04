import pygame, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel

def useTool(index: int):
    if index >= len(Global.toolBar._items) or not Global.toolBar._items[index].isReady():
        return
    Global.toolBar._items[index].use()
    Global.toolBar.removeItemByName(Global.toolBar._items[index].name)

class preview(Box):
    def __init__(self, pos, text):
        super().__init__(
            pos=pos,
            size=pygame.Vector2(200,300),
            groups=Global.uiGroup,
            color=(230, 230, 230, 255),
            border=True,
            borderColor=(50, 50, 50, 255),
            borderWidth=5,
            borderRadius=0,
        )
        Global.uiGroup.add(self, layer=10)
        self.descText = TextLabel(
            text=text,
            pos=pos,
            font_size=20,
            color=(50,50,50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(self.descText, layer = 999)
    def setPos_(self, pos):
        self.setPos(pos)
        self.descText.setPosition(pos + pygame.Vector2(10,10))
    
class Tool(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str = "",
        pos: pygame.Vector2 = pygame.Vector2(-100,-100),
        size: pygame.Vector2 = pygame.Vector2(80, 80),
        groups=None,
        imagePath: str = None,
        layer: int = 10,
        text = "",
        func = None,
        cooldown: float = 0,
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups:
                    g.add(self, layer=layer)
            else:
                groups.add(self, layer=layer)

        self.name        = name
        self.previewText = text
        self.pos         = pygame.Vector2(pos)
        self.size        = pygame.Vector2(size)
        self.imagePath   = imagePath
        self.image       = Global.loadImage(self.imagePath, (int(size.x), int(size.y)))
        self.rect        = self.image.get_rect(center=self.pos)
        self.previewBox  = None
        self.func        = func
        self.cooldown    = cooldown
        self._cdTimer    = 0
        self._cdBox      = None

    # ──────────────────────────────────────────
    # Cooldown
    # ──────────────────────────────────────────

    def triggerCooldown(self):
        self._cdTimer = self.cooldown

    def isReady(self) -> bool:
        return self._cdTimer <= 0

    def use(self):
        if not self.isReady():
            return
        if self.func:
            self.func()
        self.triggerCooldown()

    def _updateCooldownBox(self):
        if self._cdTimer <= 0:
            if self._cdBox:
                self._cdBox.kill()
                self._cdBox = None
            return

        ratio = self._cdTimer / max(self.cooldown, 0.001)
        w     = int(self.size.x)
        h     = int(self.size.y * ratio)
        y     = self.rect.top + int(self.size.y - h)   # anchored to bottom

        if not self._cdBox:
            self._cdBox = Box(
                pos=pygame.Vector2(self.rect.left, y),
                size=pygame.Vector2(w, max(1, h)),
                color=(0, 0, 0, 50),
            )
            Global.uiGroup.add(self._cdBox)
        else:
            self._cdBox.setPos(pygame.Vector2(self.rect.left, y))
            self._cdBox.setSize(pygame.Vector2(w, max(1, h)))

    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setSize(self, size):
        self.size  = pygame.Vector2(size)
        self.image = Global.loadImage(self.imagePath, (int(size.x), int(size.y)))
        self.rect  = self.image.get_rect(center=self.pos)

    def setPos(self, pos):
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

    def kill(self):
        if self._cdBox:
            self._cdBox.kill()
            self._cdBox = None
        if self.previewBox:
            self.previewBox.descText.kill()
            self.previewBox.kill()
            self.previewBox = None
        super().kill()

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self, screen=None):
        self._cdTimer -= Global.dt
        if self._cdTimer < 0:
            self._cdTimer = 0

        self._updateCooldownBox()

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.previewBox:
                self.previewBox = preview(pos=mouse_pos, text=self.previewText)
            self.previewBox.setPos_(mouse_pos - pygame.Vector2(0, self.previewBox.size.y))
        else:
            if self.previewBox:
                self.previewBox.descText.kill()
                self.previewBox.kill()
                self.previewBox = None

from Classes.Tools.BobTheBomb import bob_the_bomb
from Classes.Tools.Deflect import deflect
from Classes.Tools.Eat import eat

def foresee():
    print("see da future")

toolInfos = {
    "Bob the bomb" : {
        "Name" : "Bob the bomb",
        "Price": 120,
        "Function": bob_the_bomb,
        "ImagePath": "Assets/Tools/BobTheBomb.png",
        "Description": "Bob the bomb\n\nExplode in a\n3x3 radius\nand destroy map.",
        "CD": 3,
    },
    "Deflect" : {
        "Name" : "Deflect",
        "Price": 80,
        "Function": deflect,
        "ImagePath": "Assets/Tools/deflect.png",
        "Description": "Energy Boost\n\nEnergy gain +0.5",
        "CD": 3,
    },
    "Eat" : {
        "Name" : "Eat",
        "Price": 100,
        "Function": eat,
        "ImagePath": "Assets/Tools/eat.png",
        "Description": "Recycle\n\nNormal reload -0.2",
        "CD": 2,
    },
    "Foresee" : {
        "Name" : "Foresee",
        "Price": 120,
        "Function": foresee,
        "ImagePath": "Assets/Tools/Foresee.png",
        "Description": "Twin shots\n\nAmmo per shot +1\nEnergy cost +1",
        "CD": 10,
    },
}

class toolLoader:
    def __init__(self):
        pass
    def randomItems(self, amount):
        self.toolInfos = toolInfos.copy()
        self.itemsList = {}

        for i in range(amount):
            randomItem = random.choice(list(self.toolInfos.keys()))
            self.itemsList[i] = self.toolInfos[randomItem]
            self.itemsList[i]["Name"] = randomItem
            del self.toolInfos[randomItem]
        
        return self.itemsList