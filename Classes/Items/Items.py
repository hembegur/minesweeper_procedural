import pygame, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel

class preview(Box):
    def __init__(self, pos, text, rarity):
        super().__init__(
            pos=pos,
            size=pygame.Vector2(200,300),
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
    def setPos_(self, pos):
        self.setPos(pos)
        self.descText.setPosition(pos + pygame.Vector2(10,10))
    
class Item(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str = "",
        pos: pygame.Vector2 = pygame.Vector2(-100,-100),
        size: pygame.Vector2 = pygame.Vector2(80, 80),
        groups=None,
        imagePath: str = None,
        layer: int = 10,
        text = "",
        rarity = "Common",
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups:
                    g.add(self, layer=layer)
            else:
                groups.add(self, layer=layer)
        self.name = name
        self.previewText = text
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.imagePath = imagePath
        self.image = Global.loadImage(self.imagePath, (int(size.x), int(size.y)))
        self.rect = self.image.get_rect(center=self.pos)
        self.previewBox : preview = None
        self.rarity = rarity
    
    def setSize(self, size):
        self.size = pygame.Vector2(size)
        self.image = Global.loadImage(self.imagePath, (int(size.x), int(size.y)))
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.previewBox:
                self.previewBox = preview(pos=mouse_pos, text=self.previewText, rarity=self.rarity)
            self.previewBox.setPos_(mouse_pos - pygame.Vector2(0,self.previewBox.size.y))
        else:
            if self.previewBox:
                self.previewBox.descText.kill()
                self.previewBox.kill()
                self.previewBox = None

# ==============================COMMON==============================

def heavy_ammo():
    Global.playerStats["NormalDamage"] += 5
    Global.playerStatsLose["MP"] += 0.5
def enegy_boost():
    Global.playerStatsGain["MP"] += 0.5
def recycle():
    Global.playerStats["NormalCD"] -= 0.2 
def tough_iron():
    Global.playerStats["MaxHP"] += 8 
def hardened_iron():
    Global.playerStats["Defense"] += 3
def fuel_tank():
    Global.playerStats["MaxMP"] += 2
def auto_bot():
    Global.playerStats["HPRegen"] += 2

# ==============================Rare==============================

def twin_shot():
    Global.playerStats["Burst"] += 1
def explosive_round(): # pls add Aoe damage 
    Global.playerStatsMultiplier["NormalDamage"] -= 15
def vampire():
    Global.playerStats["LifeSteal"] += 2
def angelic_touch():
    Global.playerStats["HPRegen"] += 5

# ==============================Epic==============================

# common:
# + Tough Iron: +8 max hp
# + Hardened Iron: +3% defense
# + Fuel tank: +2 max mp
# + Auto bot: +2 hp regen
# Rare:
# + Explosive round: +1 Extra enemy hit, -15% damage
# + Vampire: +2% life steal
# + Angelic touch: +5 hp regen
# Epic:
# + One shot: +5 flat damage, +50% damage ,-3 ammo, +2 mp lose, +1.5CD
# + Glass cannon: +20% damage, -20 max hp, -10% defense
# + Rapid Trigger: +3 ammo, -0.5 mp lose, -20% damage
# + Titanium: +30 max hp, +10% defense 

itemInfos = {
    "Heavy ammo" : {
        "Name" : "Heavy ammo",
        "Price": 100,
        "Function": heavy_ammo,
        "ImagePath": "Assets/Items/heavy_ammo.png",
        "Description": "Heavy Ammo\n\nNormal damage +5\nEnergy cost +0.5",
        "Rarity": "Common",
    },
    "Energy boost" : {
        "Name" : "Energy boost",
        "Price": 120,
        "Function": enegy_boost,
        "ImagePath": "Assets/Items/energy_boost.png",
        "Description": "Energy Boost\n\nEnergy gain +0.5",
        "Rarity": "Common",
    },
    "Recycle" : {
        "Name" : "Recycle",
        "Price": 120,
        "Function": recycle,
        "ImagePath": "Assets/Items/recycle.png",
        "Description": "Recycle\n\nNormal reload -0.2",
        "Rarity": "Common",
    },
    "Twin shots" : {
        "Name" : "Twin shots",
        "Price": 250,
        "Function": twin_shot,
        "ImagePath": "Assets/Items/twin_shot.png",
        "Description": "Twin shots\n\nAmmo per shot +1\nEnergy cost +1",
        "Rarity": "Rare",
    },
}

class itemLoader:
    def __init__(self):
        pass
    def randomItems(self, amount):
        self.itemInfos = itemInfos.copy()
        self.itemsList = {}

        for i in range(amount):
            randomItem = random.choice(list(self.itemInfos.keys()))
            self.itemsList[i] = self.itemInfos[randomItem]
            self.itemsList[i]["Name"] = randomItem
            del self.itemInfos[randomItem]
        
        return self.itemsList