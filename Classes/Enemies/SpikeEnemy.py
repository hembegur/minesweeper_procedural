import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Classes.Attacks.Spike import spawnSpike
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel

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
        self.stats = Global.getEnemyStats("SpikeEnemy")
        self.pos = pygame.Vector2(pos.x,-100)
        self.ogPos = pos.copy()
        self.name = "Spike Enemy"
        self.hp = self.stats["HP"]
        self.maxHp = self.stats["HP"]
        self.money = self.stats["Money"]
        self.playJiggle(loop=True)

        self.spikeSpawnCD = self.stats["CD"]
        self.lastSpikeSpawned = self.stats["CD"]
        self.team = "Enemy"

        self._target    = None
        self._moveSpeed = 300
        self._onArrive  = None

        self.moveTo(self.ogPos, 200)

    def takeDamage(self, amount):
        self.hp -= amount

    def attack(self):
        self.pos = pygame.Vector2(Global.playerSprite.pos)
        self.rect.center = self.pos
        self.moveTo(self.ogPos, 200)

        for _ in range(20):
            particlePos = self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.mainAttackGroup, 
                pos=particlePos, 
                color=(50,50,50), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(100, 250),
                size=random.randint(50, 90),
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
            spawnSpike(onHit=self.attack, damage=self.stats["Damage"])
            spawnSpike(onHit=self.attack, damage=self.stats["Damage"])
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