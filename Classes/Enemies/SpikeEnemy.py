import pygame, Global
from Classes.BaseEntity import BaseEntity
from Classes.Attacks.Spike import spawnSpike

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
        self.hp = 25
        self.playJiggle(loop=True)

        self.spikeSpawnCD = 5
        self.lastSpikeSpawned = 0
        self.team = "Enemy"

    def takeDamage(self, amount):
        self.hp -= amount

    def update(self, dt):
        super().update(dt)  # keeps jiggle running

        if self.hp <= 0:
            self.kill()

        self.lastSpikeSpawned -= Global.dt
        if self.lastSpikeSpawned <= 0:
            spawnSpike()
            self.lastSpikeSpawned = self.spikeSpawnCD
        # your custom logic here