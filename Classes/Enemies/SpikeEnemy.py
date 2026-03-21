import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Classes.Attacks.Spike import spawnSpike
from Utils.Game.Particle import Particle

class SpikeEnemy(BaseEntity):
    def __init__(self, pos, size, groups):
        super().__init__(
            pos=pos,
            size=size,
            groups=groups,
            imagePath="Assets/Enemies/SpikeEnemy.png",
            jiggleIntensity=0.05,
            jiggleSpeed=10.0,
            jiggleAxis="both",
        )
        self.pos = pos
        self.hp = 25
        self.playJiggle(loop=True)

        self.spikeSpawnCD = Global.enemyStats["SpikeEnemy"]["CD"]
        self.lastSpikeSpawned = 0
        self.team = "Enemy"

        self._target    = None
        self._moveSpeed = 200
        self._onArrive  = None

    def takeDamage(self, amount):
        self.hp -= amount

    def attack(self):
        lastPos = self.pos.copy()
        # update BOTH pos and rect
        self.pos = pygame.Vector2(Global.playerSprite.pos)
        self.rect.center = self.pos
        self.moveTo(lastPos, 200)
        for _ in range(20):
            particlePos = self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.mainAttackGroup, 
                pos=particlePos, 
                color=(50,50,50), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(50, 150),
                size=random.randint(20, 60),
                fadeSpeed=500,
            )

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

    def update(self):
        super().update()  # keeps jiggle running

        if self.hp <= 0:
            self.kill()

        self.lastSpikeSpawned -= Global.dt
        if self.lastSpikeSpawned <= 0:
            spawnSpike(onHit=self.attack, damage=Global.enemyStats["SpikeEnemy"]["Damage"])
            self.lastSpikeSpawned = self.spikeSpawnCD
        # your custom logic here

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