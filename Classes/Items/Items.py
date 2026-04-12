import pygame, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel

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
    Global.playerStatsGain["MP"] += 1
def recycle():
    Global.playerStats["AttackSpeed"] += 10
    Global.playerStats["BurstAttackSpeed"] += 20
def tough_iron():
    Global.playerStats["MaxHP"] += 8 
def hardened_iron():
    Global.playerStats["Defense"] += 3
def fuel_tank():
    Global.playerStats["MaxMP"] += 2
def auto_bot():
    Global.playerStats["HPRegen"] += 2

# ==============================RARE==============================

def twin_shot():
    Global.playerStats["Burst"] += 1
    Global.playerStats["BurstAttackSpeed"] += 100
def explosive_round():
    Global.playerStatsMultiplier["NormalDamage"] -= 15
    Global.playerStats["Aoe"] += 1
def vampire():
    Global.playerStats["LifeSteal"] += 2
def angelic_touch():
    Global.playerStats["HPRegen"] += 5
    Global.playerStatsGain["MP"] += 1.5

# ==============================EPIC==============================

def one_shot():
    Global.playerStats["NormalDamage"] += 12
    Global.playerStatsMultiplier["NormalDamage"] += 40
    Global.playerStats["Burst"] -= 3
    Global.playerStats["BurstAttackSpeed"] -= 100
    if Global.playerStats["Burst"] <= 0:
        Global.playerStats["Burst"] = 1
    Global.playerStatsLose["MP"] += 1.5
    Global.playerStats["AttackSpeed"] -= 25
def glass_cannon():
    Global.playerStatsMultiplier["NormalDamage"] += 20
    Global.playerStats["MaxHP"] -= 20
    Global.playerStats["Defense"] -= 10
def rapid_trigger():
    Global.playerStats["Burst"] += 3
    Global.playerStatsLose["MP"] -= 0.2
    if Global.playerStatsLose["MP"] <= 0.5:
        Global.playerStatsLose["MP"] = 0.5
    Global.playerStatsMultiplier["NormalDamage"] -= 20
    Global.playerStats["BurstAttackSpeed"] += 150
def titanium():
    Global.playerStats["MaxHP"] += 30
    Global.playerStats["Defense"] += 10

itemInfos = {
    # ==============================COMMON==============================
    "Heavy ammo" : {
        "Name" : "Heavy ammo",
        "Price": 80,
        "Function": heavy_ammo,
        "ImagePath": "Assets/Items/heavy_ammo.png",
        "Description": "Heavy Ammo\n\nNormal damage +5\nMP cost +0.5",
        "Rarity": "Common",
    },
    "Energy boost" : {
        "Name" : "Energy boost",
        "Price": 70,
        "Function": enegy_boost,
        "ImagePath": "Assets/Items/energy_boost.png",
        "Description": "Energy Boost\n\nMP gain +1",
        "Rarity": "Common",
    },
    "Recycle" : {
        "Name" : "Recycle",
        "Price": 60,
        "Function": recycle,
        "ImagePath": "Assets/Items/recycle.png",
        "Description": "Recycle\n\nAttack speed +10",
        "Rarity": "Common",
    },
    "Tough iron": {
        "Name": "Tough iron",
        "Price": 60,
        "Function": tough_iron,
        "ImagePath": "Assets/Items/tough_iron.png",
        "Description": "Tough Iron\n\nMax HP +8",
        "Rarity": "Common",
    },
    "Hardened iron": {
        "Name": "Hardened iron",
        "Price": 60,
        "Function": hardened_iron,
        "ImagePath": "Assets/Items/hardened_iron.png",
        "Description": "Hardened Iron\n\nDefense +3",
        "Rarity": "Common",
    },
    "Fuel tank": {
        "Name": "Fuel tank",
        "Price": 60,
        "Function": fuel_tank,
        "ImagePath": "Assets/Items/fuel_tank.png",
        "Description": "Fuel Tank\n\nMax energy +2",
        "Rarity": "Common",
    },
    "Auto bot": {
        "Name": "Auto bot",
        "Price": 70,
        "Function": auto_bot,
        "ImagePath": "Assets/Items/auto_bot.png",
        "Description": "Auto Bot\n\nHP regen +2",
        "Rarity": "Common",
    },
    # ==============================RARE==============================
    "Twin shots" : {
        "Name" : "Twin shots",
        "Price": 120,
        "Function": twin_shot,
        "ImagePath": "Assets/Items/twin_shot.png",
        "Description": "Twin shots\n\nBurst +1",
        "Rarity": "Rare",
    },
    "Explosive round": {
        "Name": "Explosive round",
        "Price": 120,
        "Function": explosive_round,
        "ImagePath": "Assets/Items/explosive_round.png",
        "Description": "Explosive round\n\n+1 enemy hit (AoE)\nDamage -15%",
        "Rarity": "Rare",
    },
    "Vampire": {
        "Name": "Vampire",
        "Price": 110,
        "Function": vampire,
        "ImagePath": "Assets/Items/vampire.png",
        "Description": "Vampire\n\nLife steal +2%",
        "Rarity": "Rare",
    },
    "Angelic touch": {
        "Name": "Angelic touch",
        "Price": 135,
        "Function": angelic_touch,
        "ImagePath": "Assets/Items/angelic_touch.png",
        "Description": "Angelic Touch\n\nHP regen +5\nMP gain +1.5",
        "Rarity": "Rare",
    },

    # ==============================EPIC==============================
    "One shot": {
        "Name": "One shot",
        "Price": 300,
        "Function": one_shot,
        "ImagePath": "Assets/Items/one_shot.png",
        "Description": "One Shot\n\n+12 damage\n+40% damage\nBurst -3 (min 1)\nMP cost +1.5\nAttack speed -25",
        "Rarity": "Epic",
    },
    "Glass cannon": {
        "Name": "Glass cannon",
        "Price": 250,
        "Function": glass_cannon,
        "ImagePath": "Assets/Items/glass_cannon.png",
        "Description": "Glass Cannon\n\nDamage +20%\nMax HP -20\nDefense -10",
        "Rarity": "Epic",
    },
    "Rapid trigger": {
        "Name": "Rapid trigger",
        "Price": 280,
        "Function": rapid_trigger,
        "ImagePath": "Assets/Items/rapid_trigger.png",
        "Description": "Rapid Trigger\n\nBurst +3\nMP cost -0.2 (min 0.5)\nDamage -20%",
        "Rarity": "Epic",
    },
    "Titanium": {
        "Name": "Titanium",
        "Price": 270,
        "Function": titanium,
        "ImagePath": "Assets/Items/titanium.png",
        "Description": "Titanium\n\nMax HP +30\nDefense +10",
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


class itemLoader:
    def __init__(self):
        pass

    def randomItems(self, amount):
        self.itemInfos = itemInfos.copy()
        self.itemsList = {}

        for i in range(amount):
            if not self.itemInfos:
                break
            randomItem = _weightedRandom(self.itemInfos)
            self.itemsList[i] = self.itemInfos[randomItem].copy()
            self.itemsList[i]["Name"] = randomItem
            del self.itemInfos[randomItem]

        return self.itemsList