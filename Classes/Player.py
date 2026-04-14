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
            pos=self.pos + pygame.Vector2(300,0),
            group=Global.mainAttackGroup,
            layer=999
        )

        self.shootTimer : pygame.sprite.Group = pygame.sprite.Group()
        self.passiveHeal = 0
        self.hpCheckText = TextLabel(
            text="",
            pos=pygame.Vector2(0,0),
            font_size=20,
            color=(255,0,0),
            font_name="Assets/Fonts/Minecraft.ttf",
            center=True,
        )
        Global.uiGroup.add(self.hpCheckText, layer = 999)

    def takeDamage(self, amount):
        Global.SoundManager.playSFX("Assets/Sounds/SoundEffect/hurt.wav", 0.3)
        actualAmount = amount - max(amount * 0.8, amount * Global.playerStats["Defense"]/100)
        Global.playerStats["HP"] -= actualAmount
        text_label = TextLabel(
            text=f"-{round(actualAmount,1):g}HP",
            pos=self.pos,
            font_size=30,
            color=(225,0,0),
            font_name="Assets/Fonts/Minecraft.ttf",
            center=True,
        )
        text_label.moveTo(self.pos - pygame.Vector2(0,50), speed=300)
        text_label.fadeOut(speed=300, onDone=text_label.kill)
        Global.uiGroup.add(text_label)

    def handleEvents(self, event: pygame.event.get):
        def checkClosest():
            mouse_pos = pygame.mouse.get_pos()
            if not Global.mainGameBox.rect.collidepoint(mouse_pos): 
                return
            
            closest = None
            for sprite in Global.entityGroup:
                if sprite.team == "Enemy":
                    if not closest:
                        if (sprite.pos - mouse_pos).length() < 100:
                            closest = sprite
                    elif 100 > (closest.pos - mouse_pos).length() > (sprite.pos - mouse_pos).length():
                        closest = sprite
            if closest:
                return closest
            return None
        
        #hover to check hp
        hpCheckEnemy = checkClosest()
        if hpCheckEnemy:
            self.hpCheckText.setPosition(pygame.mouse.get_pos())
            self.hpCheckText.setText(f"{hpCheckEnemy.name} ({round(hpCheckEnemy.hp,1):g}/{hpCheckEnemy.maxHp})")
        else:
            self.hpCheckText.setText(f"")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            closest = checkClosest()
            self.currentTarget = closest

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f and Global.playerStats["Ult"] >= Global.playerStatsLose["Ult"]: #ultimate
            def hit():
                for sprite in Global.entityGroup:
                    if sprite.team == "Enemy":
                        text_label = TextLabel(
                            text=f"-{round(Global.playerStats["NormalDamage"] * 3,1):g}HP",
                            pos=sprite.pos,
                            font_size=20,
                            color=(225,0,0),
                            font_name="Assets/Fonts/Minecraft.ttf",
                            center=True,
                        )
                        text_label.moveTo(sprite.pos - pygame.Vector2(0,50), speed=300)
                        text_label.fadeOut(speed=300, onDone=text_label.kill)
                        Global.uiGroup.add(text_label)
                        sprite.takeDamage(Global.playerStats["NormalDamage"] * 3)
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
        self.shootTimer.update()
        self.attackJiggle.update(Global.dt)
        self.lastAttack -= Global.dt
        if self.currentTarget:
            self.attackPointer.pos = self.currentTarget.pos

        if Global.playerStats["HP"] >= Global.playerStats["MaxHP"]:
            Global.playerStats["HP"] = Global.playerStats["MaxHP"]
        if Global.playerStats["MP"] >= Global.playerStats["MaxMP"]:
            Global.playerStats["MP"] = Global.playerStats["MaxMP"]

        self.passiveHeal -= Global.dt
        if self.passiveHeal <= 0 and Global.playerStats["HPRegen"] > 0 and Global.playerStats["HP"] < Global.playerStats["MaxHP"]:
            self.passiveHeal = 10 / Global.playerStats["HPRegen"]
            Global.playerStats["HP"] += 1

        if self.lastAttack <= 0 and Global.playerStats["MP"] >= Global.playerStatsLose["MP"]:
            if len(Global.entityGroup) <= 0:
                self.currentTarget = None
            if self.currentTarget and not self.currentTarget.alive():
                self.currentTarget = None
            if self.currentTarget:
                def shoot():
                    if not Global.playerStats["MP"] >= Global.playerStatsLose["MP"] or not self.currentTarget:
                        self.shootTimer.empty()
                        return
                    self.lastAttack = Global.playerStats["BaseAttackSpeed"] / Global.playerStats["AttackSpeed"]

                    Global.playerStats["MP"] -= Global.playerStatsLose["MP"]
                    target = self.currentTarget
                    damageCalc = Global.playerStats["NormalDamage"] + Global.playerStats["NormalDamage"] * Global.playerStatsMultiplier["NormalDamage"]/100
                    def hit(pos = target.pos, first = True, damage=damageCalc):
                        Global.playerStats["HP"] += damage * Global.playerStats["LifeSteal"]/100
                        text_label = TextLabel(
                            text=f"-{round(damage,1):g}HP",
                            pos=pos,
                            font_size=20,
                            color=(225,0,0),
                            font_name="Assets/Fonts/Minecraft.ttf",
                            center=True,
                        )
                        text_label.moveTo(pos - pygame.Vector2(0,50), speed=300)
                        text_label.fadeOut(speed=300, onDone=text_label.kill)
                        Global.uiGroup.add(text_label)
                        target.takeDamage(damage)
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

                        if first:
                            enemies = [e for e in Global.entityGroup if e.team == "Enemy" and e != target]
                            enemies.sort(key=lambda e: (e.pos - pos).length())

                            falloff = 0.7
                            i = 0
                            while i < min(Global.playerStats["Aoe"], len(enemies)):
                                e = enemies[i]
                                #e.takeDamage(damage * (falloff ** (i + 1)))
                                hit(e.pos, False, damage * (falloff ** (i + 1)))
                                i += 1
                            
                    self.attackJiggle.play(loop=False)
                    newBullet = Bullet(
                        size=pygame.Vector2(100,150),
                        ogPos=self.pos + pygame.Vector2(100,0),
                        targetPos=target.pos,
                        speed=1000,
                    )
                    newBullet._onArrive = hit
                    Global.mainAttackGroup.add(newBullet)
                    
                    if self.currentTarget.hp - damageCalc <= 0: 
                        found = False
                        for sprite in Global.entityGroup:
                            if sprite.team == "Enemy" and sprite != self.currentTarget:
                                self.currentTarget = sprite
                                found = True
                                break
                        if not found:
                            self.currentTarget = None
                #shoot()
                for i in range(Global.playerStats["Burst"]):
                    Timer(Global.playerStats["BaseAttackSpeed"] / Global.playerStats["BurstAttackSpeed"] * i, shoot, self.shootTimer)
                
            else:
                found = False
                for sprite in Global.entityGroup:
                    if sprite.team == "Enemy":
                        self.currentTarget = sprite
                        found = True
                        break
                if not found:
                    self.currentTarget = None