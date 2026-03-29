import pygame, Global, random

class SimpleItem(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2 = pygame.Vector2(-100,-100),
        size: pygame.Vector2 = pygame.Vector2(80, 80),
        groups=None,
        imagePath: str = None,
        layer: int = 0,
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups:
                    g.add(self, layer=layer)
            else:
                groups.add(self, layer=layer)

        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.imagePath = imagePath
        self.image = Global.loadImage(imagePath, (int(size.x), int(size.y)))
        self.rect = self.image.get_rect(center=self.pos)

class heavy_ammo(SimpleItem):
    def __init__(self):
        super().__init__(
            groups=Global.uiGroup,
            imagePath="Assets/Items/heavy_ammo.png",
        )
        Global.playerStats["NormalDamage"] += 5
        Global.playerStatsLose["MP"] += 0.5

class enegy_boost(SimpleItem):
    def __init__(self):
        super().__init__(
            groups=Global.uiGroup,
            imagePath="Assets/Items/energy_boost.png",
        )
        Global.playerStatsGain["MP"] += 0.5

class recycle(SimpleItem):
    def __init__(self):
        super().__init__(
            groups=Global.uiGroup,
            imagePath="Assets/Items/recycle.png",
        )
        Global.playerStats["NormalCD"] -= 0.2 

class twin_shot(SimpleItem):
    def __init__(self):
        super().__init__(
            groups=Global.uiGroup,
            imagePath="Assets/Items/twin_shot.png",
        )
        Global.playerStats["NormalDamage"] += 5

itemInfos = {
    "Heavy ammo" : {
        "Price": 100,
        "Link": heavy_ammo,
        "ImagePath": "Assets/Items/heavy_ammo.png",
    },
    "Energy boost" : {
        "Price": 120,
        "Link": enegy_boost,
        "ImagePath": "Assets/Items/energy_boost.png",
    },
    "Recycle" : {
        "Price": 120,
        "Link": recycle,
        "ImagePath": "Assets/Items/recycle.png",
    },
    "Twin shots" : {
        "Price": 150,
        "Link": twin_shot,
        "ImagePath": "Assets/Items/twin_shot.png",
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