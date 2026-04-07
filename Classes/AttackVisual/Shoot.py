import pygame, Global, random, math
from Utils.Game.mathStuff import getAngle
from Utils.Game.Particle import Particle
from Utils.Game.mathStuff import getDirection

class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        size,
        ogPos,
        targetPos,
        speed,
        onArrive = None,
    ):
        super().__init__()
        self.size = size
        self.ogImage = Global.loadImage("Assets/Projectiles/Bullet.png", (int(size.x), int(size.y)))
        self.image = pygame.transform.rotate(self.ogImage, -getAngle(ogPos, targetPos)) 
        self.rect = self.image.get_rect(center=ogPos)
        self.pos = ogPos.copy()
        self.ogPos = ogPos.copy()
        self._target = targetPos.copy()
        self._moveSpeed = speed
        self._onArrive = onArrive

        self.lastParticle1 = 0
        self.particle1CD = 0.1
        
    def update(self):
        self.lastParticle1 -= Global.dt

        if self.lastParticle1 <= 0:
            self.lastParticle1 = self.particle1CD
            Particle(
                groups=Global.mainAttackGroup, 
                pos=self.pos.copy(), 
                color=(200, 140, 0), 
                direction=getDirection(self.pos, self.ogPos), 
                speed=random.randint(50, 100),
                size=random.randint(30,45),
                fadeSpeed=500,
            )
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

            # update rect
            self.rect.center = self.pos