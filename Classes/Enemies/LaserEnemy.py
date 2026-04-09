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
        self.pos = pygame.Vector2(pos.x,-100)
        self.ogPos = pos.copy()
        self.hp = Global.enemyStats["LaserEnemy"]["HP"]
        self.playJiggle(loop=True)

        self.spikeSpawnCD = Global.enemyStats["LaserEnemy"]["CD"]
        self.lastSpikeSpawned = Global.enemyStats["LaserEnemy"]["CD"]
        self.team = "Enemy"

        self._target    = None
        self._moveSpeed = 300
        self._onArrive  = None

        self.moveTo(self.ogPos, 200)

    def takeDamage(self, amount):
        self.hp -= amount

    def moveTo(
        self,
        destination: pygame.Vector2,
        speed: float,
        onArrive=None,       # optional callback when destination reached
    ):
        """Move label toward destination at given speed (px/sec)."""
        self._target    = pygame.Vector2(destination)
        self._moveSpeed = speed
        self._onArrive  = onArrive

    def attack(self):
        playerPos = Global.playerSprite.pos
        laser = Laser(pos1=self.pos, pos2=playerPos, groups=Global.mainAttackGroup, width=30, color=(100,100,255))
        laser.shrinkAndFade(targetWidth=0, shrinkSpeed=60, targetAlpha=0, fadeSpeed=510, onDone=laser.kill)

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
            for _ in range(2):
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

        # ── movement ──
        if self._target is not None:
            delta = self._target - self.pos
            dist  = delta.length()
            step  = self._moveSpeed * Global.dt

            if dist <= step:
                # arrived
                self.pos = pygame.Vector2(self._target)
                self._target = None
                if self._onArrive:
                    self._onArrive()
            else:
                self.pos += delta.normalize() * step

            self.rect.center = self.pos