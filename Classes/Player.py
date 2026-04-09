import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.UiComponents.TextLabel import TextLabel
from Classes.AttackVisual.Shoot import Bullet
from Utils.Game.Particle import Particle
from Utils.Game.Jiggle import Jiggle
from Utils.Game.mathStuff import Timer
from Classes.AttackVisual.Pointer import Pointer

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
        self.currentTarget = None

        self.attackJiggle = Jiggle(
            sprite=self,
            intensity=0.2,
            speed=30.0,
            axis="both"
        )
        self.attackJiggle._ogImage  = self.image.copy()
        self.attackJiggle._ogSize   = pygame.Vector2(self.size)
        self.attackPointer = Pointer(
            size=pygame.Vector2(350,350),
            speed=200,
            pos=self.pos,
            group=Global.mainAttackGroup,
            layer=999
        )

    def takeDamage(self, amount):
        Global.playerStats["HP"] -= amount

    def handleEvents(self, event: pygame.event.get):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if not Global.mainGameBox.rect.collidepoint(mouse_pos): 
                return
            
            closest = None
            for sprite in Global.entityGroup:
                if sprite.team == "Enemy":
                    if not closest:
                        closest = sprite
                    elif (closest.pos - mouse_pos).length() > (sprite.pos - mouse_pos).length():
                        closest = sprite
            if closest:
                self.currentTarget = closest

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f and Global.playerStats["Ult"] >= Global.playerStatsLose["Ult"]: #ultimate
            def hit():
                for sprite in Global.entityGroup:
                    if sprite.team == "Enemy":
                        text_label = TextLabel(
                            text=f"-{Global.playerStats["UltDamage"]}HP",
                            pos=sprite.pos,
                            font_size=20,
                            color=(225,0,0),
                            font_name="Assets/Fonts/Minecraft.ttf",
                            center=True,
                        )
                        text_label.moveTo(sprite.pos - pygame.Vector2(0,50), speed=300)
                        text_label.fadeOut(speed=300, onDone=text_label.kill)
                        Global.uiGroup.add(text_label)
                        sprite.takeDamage(Global.playerStats["UltDamage"])
                newBullet.kill()

                for _ in range(20):
                    particlePos = newBullet.pos[0] + random.randint(-20, 20), newBullet.pos[1] + random.randint(-20, 20)
                    Particle(
                        groups=Global.mainAttackGroup, 
                        pos=particlePos, 
                        color=(200,150,0), 
                        direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                                    math.sin(random.uniform(0, 2 * math.pi))), 
                        speed=random.randint(250, 450),
                        size=random.randint(100, 200),
                        fadeSpeed=500,
                    )

            Global.playerStats["Ult"] -= Global.playerStatsLose["Ult"]

            self.attackJiggle.play(loop=False)
            newBullet = Bullet(
                size=pygame.Vector2(100,150),
                ogPos=self.pos + pygame.Vector2(100,0),
                targetPos=self.currentTarget.pos if self.currentTarget else self.pos + pygame.Vector2(300,0),
                speed=500,
            )
            newBullet._onArrive = hit
            Global.mainAttackGroup.add(newBullet)

    def update(self):
        super().update()
        self.attackJiggle.update(Global.dt)
        self.lastAttack -= Global.dt
        if self.currentTarget:
            self.attackPointer.pos = self.currentTarget.pos

        if self.lastAttack <= 0 and Global.playerStats["MP"] >= Global.playerStatsLose["MP"] * Global.playerStats["Burst"]:
            if len(Global.entityGroup) <= 0:
                self.currentTarget = None
            if self.currentTarget and not self.currentTarget.alive():
                self.currentTarget = None
            if self.currentTarget:
                self.lastAttack = Global.playerStats["BaseAttackSpeed"] / Global.playerStats["AttackSpeed"]

                def shoot():
                    Global.playerStats["MP"] -= Global.playerStatsLose["MP"]
                    target = self.currentTarget
                    def hit():
                        text_label = TextLabel(
                            text=f"-{Global.playerStats["NormalDamage"]}HP",
                            pos=target.pos,
                            font_size=20,
                            color=(225,0,0),
                            font_name="Assets/Fonts/Minecraft.ttf",
                            center=True,
                        )
                        text_label.moveTo(target.pos - pygame.Vector2(0,50), speed=300)
                        text_label.fadeOut(speed=300, onDone=text_label.kill)
                        Global.uiGroup.add(text_label)
                        target.takeDamage(Global.playerStats["NormalDamage"])
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
                            
                    self.attackJiggle.play(loop=False)
                    newBullet = Bullet(
                        size=pygame.Vector2(100,150),
                        ogPos=self.pos + pygame.Vector2(100,0),
                        targetPos=target.pos,
                        speed=500,
                    )
                    newBullet._onArrive = hit
                    Global.mainAttackGroup.add(newBullet)

                    if self.currentTarget.hp - Global.playerStats["NormalDamage"] <= 0:
                        for sprite in Global.entityGroup:
                            if sprite.team == "Enemy" and sprite != self.currentTarget:
                                self.currentTarget = sprite
                                break
                #shoot()
                for i in range(Global.playerStats["Burst"]):
                    Timer(Global.playerStats["BaseAttackSpeed"] / Global.playerStats["BurstAttackSpeed"] * i, shoot, Global.timerGroup)
                
            else:
                for sprite in Global.entityGroup:
                    if sprite.team == "Enemy":
                        self.currentTarget = sprite
                        break
                