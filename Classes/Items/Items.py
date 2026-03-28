import pygame, Global

class itemLoader:
    def __init__(self):
        pass

class SimpleItem(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2 = pygame.Vector2(0,0),
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
            imagePath="Assets/Items/enegy_boost.png",
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


