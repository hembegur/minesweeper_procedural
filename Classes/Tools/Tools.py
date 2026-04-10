import pygame, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel

def useTool(index: int):
    if index >= len(Global.toolBar._items) or not Global.toolBar._items[index].isReady():
        return
    Global.toolBar._items[index].use()
    Global.toolBar.removeItemByName(Global.toolBar._items[index].name)

class preview(Box):
    def __init__(self, pos, text, rarity):
        super().__init__(
            pos=pos,
            size=pygame.Vector2(350,300),
            groups=Global.uiGroup,
            color=Global.rarityColor[rarity]["color"],
            border=True,
            borderColor=Global.rarityColor[rarity]["borderColor"],
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
        self.sellText = TextLabel(
            text="[X] sell",
            pos=pos + pygame.Vector2(0,250),
            font_size=20,
            color=(150,0,0),
            font_name="Assets/Fonts/Rimouski.otf",
            center=False,
        )
        Global.uiGroup.add(self.sellText, layer = 999)
    def setPos_(self, pos):
        self.setPos(pos)
        self.descText.setPosition(pos + pygame.Vector2(10,10))
        self.sellText.setPosition(pos + pygame.Vector2(10,265))

    def kill(self):
        self.descText.kill()
        self.sellText.kill()
        super().kill()
    
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
        rarity = "Common",
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
        self.rarity = rarity

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
                color=(0, 0, 0, 150),
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
                self.previewBox = preview(pos=mouse_pos, text=self.previewText, rarity=self.rarity)
            self.previewBox.setPos_(mouse_pos - pygame.Vector2(0, self.previewBox.size.y))
        else:
            if self.previewBox:
                self.previewBox.kill()
                self.previewBox = None


def sellTool():
    mouse_pos = pygame.mouse.get_pos()
    for tool in Global.toolBar._items:
        if tool.rect.collidepoint(mouse_pos):
            Global.toolBar.removeItemByName(tool.name)
            break

from Classes.Tools.BobTheBomb import bob_the_bomb
from Classes.Tools.Deflect import deflect
from Classes.Tools.Eat import eat
from Classes.Tools.Foresee import foresee
from Classes.Tools.Nuke import nuke
from Classes.Tools.ConentratedBeam import concentrated_beam
from Classes.Tools.Adrenaline import adrenaline

toolInfos = {
    "Bob the bomb" : {
        "Name" : "Bob the bomb",
        "Price": 120,
        "Function": bob_the_bomb,
        "ImagePath": "Assets/Tools/BobTheBomb.png",
        "Description": "Bob the bomb\n\nExplode in a 3x3 radius cross \nshape and destroy map.\n\nCD: 3",
        "CD": 3,
        "Rarity": "Common",
    },
    "Eat" : {
        "Name" : "Eat",
        "Price": 100,
        "Function": eat,
        "ImagePath": "Assets/Tools/eat.png",
        "Description": "Eat\n\nUsed on bomb tile: +1/5 max hp\nUsed on normal tile: -1/10 max hp\nUsed on revealed tile: Nothing\n\nCD: 2",
        "CD": 2,
        "Rarity": "Common",
    },
    "Deflect" : {
        "Name" : "Deflect",
        "Price": 80,
        "Function": deflect,
        "ImagePath": "Assets/Tools/deflect.png",
        "Description": "Defleat\n\nReleases an engergy blast that\ndestroy enemy projectiles.\n\nCD: 3",
        "CD": 3,
        "Rarity": "Rare",
    },
    "Concentrated beam" : {
        "Name" : "Concentrated beam",
        "Price": 80,
        "Function": concentrated_beam,
        "ImagePath": "Assets/Tools/concentrated_beam.png",
        "Description": "Concentrated beam\n\nFocuses a beam that deals 3\ntimes of your damage onto the\ncurrent target.\n\nCD: 3",
        "CD": 3,
        "Rarity": "Rare",
    },
    "Adrenaline" : {
        "Name" : "Adrenaline",
        "Price": 80,
        "Function": adrenaline,
        "ImagePath": "Assets/Tools/adrenaline.png",
        "Description": "Adrenaline\n\nSlow everything down to x0.4\nTemporary x2 MP gain\nDuration: 8 seconds\n\nCD: 10",
        "CD": 10,
        "Rarity": "Rare",
    },
    "Foresee" : {
        "Name" : "Foresee",
        "Price": 120,
        "Function": foresee,
        "ImagePath": "Assets/Tools/Foresee.png",
        "Description": "Foresee\n\nIn the range of 5x5 pick 5 random\ntiles to reveal with the accuracy of\n90%\n\nCD: 20",
        "CD": 20,
        "Rarity": "Epic",
    },
    "Nuke" : {
        "Name" : "Nuke",
        "Price": 150,
        "Function": nuke,
        "ImagePath": "Assets/Tools/nuclear.png",
        "Description": "Nuke\n\nNuke everything in the 7x7\n\nCD: 10",
        "CD": 10,
        "Rarity": "Epic",
    },
}
def _weightedRandom(infos: dict) -> str:
    """Pick a random key from infos based on its Rarity field and currentRarity weights."""
    keys = list(infos.keys())
    weights = [
        Global.currentRarity.get(infos[k].get("Rarity", "Common"), 60)
        for k in keys
    ]
    return random.choices(keys, weights=weights, k=1)[0]
class toolLoader:
    def __init__(self):
        pass

    def randomItems(self, amount):
        self.toolInfos = toolInfos.copy()
        self.itemsList = {}

        for i in range(amount):
            if not self.toolInfos:
                break
            randomItem = _weightedRandom(self.toolInfos)
            self.itemsList[i] = self.toolInfos[randomItem].copy()
            self.itemsList[i]["Name"] = randomItem
            del self.toolInfos[randomItem]

        return self.itemsList