import pygame, Global
from Classes.BaseEntity import BaseEntity

class PlayerSprite(BaseEntity):
    def __init__(self, pos, size, groups):
        super().__init__(
            pos=pos,
            size=size,
            groups=groups,
            imagePath="Assets/Player.png",
            jiggleIntensity=0.05,
            jiggleSpeed=10.0,
            jiggleAxis="both",
        )
        self.hp = 100
        self.playJiggle(loop=True)

    def takeDamage(self, amount):
        self.hp -= amount

    def update(self, dt):
        super().update(dt)  # keeps jiggle running
        
        for sprite in Global.entityGroup:
            if sprite.team == "Enemy":
                print("die niger")