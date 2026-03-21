import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Classes.Attacks.Laser import spawnLaser, Laser
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel

class LaserEnemy(BaseEntity):
    def __init__(self, pos, size, groups):
        super().__init__(
            pos=pos,
            size=size,
            groups=groups,
            imagePath="Assets/Enemies/LaserEnemy.png",
            jiggleIntensity=0.05,
            jiggleSpeed=10.0,
            jiggleAxis="both",
        )
        self.hp = 25
        self.playJiggle(loop=True)

        self.spikeSpawnCD = Global.enemyStats["LaserEnemy"]["CD"]
        self.lastSpikeSpawned = 0
        self.team = "Enemy"

    def takeDamage(self, amount):
        self.hp -= amount

    def attack(self):
        playerPos = Global.playerSprite.pos
        laser = Laser(pos1=self.pos, pos2=playerPos, groups=Global.mainAttackGroup, width=30, color=(100,100,255))
        laser.shrinkAndFade(targetWidth=0, shrinkSpeed=60, targetAlpha=0, fadeSpeed=510, onDone=laser.kill)

        text_label = TextLabel(
            text=f"-{Global.enemyStats["LaserEnemy"]["Damage"]}HP",
            pos=playerPos,
            font_size=30,
            color=(225,0,0),
            font_name="Assets/Fonts/Minecraft.ttf",
            center=True,
        )
        text_label.moveTo(playerPos - pygame.Vector2(0,50), speed=300)
        text_label.fadeOut(speed=300, onDone=text_label.kill)
        Global.uiGroup.add(text_label)

        for _ in range(20):
            particlePos = playerPos[0] + random.randint(-20, 20), playerPos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.mainAttackGroup, 
                pos=particlePos, 
                color=(50,50,255), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(100, 250),
                size=random.randint(30, 60),
                fadeSpeed=500,
            )

    def update(self):
        super().update()  # keeps jiggle running

        if self.hp <= 0:
            self.kill()

        self.lastSpikeSpawned -= Global.dt
        if self.lastSpikeSpawned <= 0:
            axis = random.choice(["horizontal", "vertical"])
            spawnLaser(
                surfaceSize=Global.minesweeperSurfaceSize,
                groups=Global.msAttackGroup,
                warningDuration=1,
                warningColor=(255, 50, 50),
                laserColor=(60,60,200),
                laserWidth=50,
                laserDuration=0.6,
                damage = Global.enemyStats["LaserEnemy"]["Damage"],
                axis=axis,
                onHit=self.attack
            )
            self.lastSpikeSpawned = self.spikeSpawnCD
        # your custom logic here