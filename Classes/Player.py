import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.UiComponents.TextLabel import TextLabel
from Classes.AttackVisual.Shoot import Bullet
from Utils.Game.Particle import Particle
from Utils.Game.Jiggle import Jiggle
from Utils.Game.mathStuff import getDirection

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
        self.lastAttack = 0

        self.attackJiggle = Jiggle(
            sprite=self,
            intensity=0.2,
            speed=30.0,
            axis="both"  # ← lowercase
        )
        self.attackJiggle._ogImage  = self.image.copy()
        self.attackJiggle._ogSize   = pygame.Vector2(self.size)

    def takeDamage(self, amount):
        Global.playerStats["HP"] -= amount

    def update(self):
        super().update()
        self.attackJiggle.update(Global.dt)
        self.lastAttack -= Global.dt
        if self.lastAttack <= 0 and Global.playerStats["MP"] >= Global.playerStatsLose["MP"]:
            for sprite in Global.entityGroup:
                if sprite.team == "Enemy":
                    def hit():
                        text_label = TextLabel(
                            text=f"-{Global.playerStats["NormalDamage"]}HP",
                            pos=sprite.pos,
                            font_size=20,
                            color=(225,0,0),
                            font_name="Assets/Fonts/Minecraft.ttf",
                            center=True,
                        )
                        text_label.moveTo(sprite.pos - pygame.Vector2(0,50), speed=300)
                        text_label.fadeOut(speed=300, onDone=text_label.kill)
                        Global.uiGroup.add(text_label)
                        sprite.takeDamage(Global.playerStats["NormalDamage"])
                        newBullet.kill()

                        for _ in range(20):
                            particlePos = newBullet.pos[0] + random.randint(-20, 20), newBullet.pos[1] + random.randint(-20, 20)
                            Particle(
                                groups=Global.mainAttackGroup, 
                                pos=particlePos, 
                                color=(100,50,0), 
                                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                                         math.sin(random.uniform(0, 2 * math.pi))), 
                                speed=random.randint(50, 150),
                                size=random.randint(20, 60),
                                fadeSpeed=500,
                            )

                    Global.playerStats["MP"] -= Global.playerStatsLose["MP"]
                    self.lastAttack = Global.playerStats["NormalCD"]

                    self.attackJiggle.play(loop=False)
                    newBullet = Bullet(
                        size=pygame.Vector2(100,150),
                        ogPos=self.pos + pygame.Vector2(100,0),
                        targetPos=sprite.pos,
                        speed=500,
                    )
                    newBullet._onArrive = hit
                    Global.mainAttackGroup.add(newBullet)
                    break