import pygame, Global
from Classes.BaseEntity import BaseEntity
from Utils.UiComponents.TextLabel import TextLabel

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

        self.attackCD = 2
        self.lastAttack = 0

    def takeDamage(self, amount):
        self.hp -= amount

    def update(self, dt):
        super().update(dt)  # keeps jiggle running

        self.lastAttack -= Global.dt
        while self.lastAttack <= 0 and Global.playerMP >= 5:
            self.lastAttack += self.attackCD
            Global.playerMP -= 5

            for sprite in Global.entityGroup:
                if sprite.team == "Enemy":
                    text_label = TextLabel(
                        text="-10HP",
                        pos=sprite.pos,
                        font_size=20,
                        color=(225,0,0),
                        font_name="Assets/Fonts/Minecraft.ttf",
                        center=True,
                    )
                    text_label.moveTo(sprite.pos - pygame.Vector2(0,50), speed=300)
                    text_label.fadeOut(speed=300, onDone=text_label.kill)
                    Global.uiGroup.add(text_label)

                    sprite.takeDamage(10)

                    break