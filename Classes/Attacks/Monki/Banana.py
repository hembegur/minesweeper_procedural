import pygame, Global, random
from Utils.Game.mathStuff import randomEdgePos, getDirection
from Utils.Game.Particle import Particle
from Utils.Game.mathStuff import Timer

def spawnBanana(onHit, damage):
    screenWidth = int(Global.minesweeperSurfaceSize.x)
    screenHeight = int(Global.minesweeperSurfaceSize.y)
    pos = randomEdgePos(screenWidth,screenHeight)
    newBanana = Banana(
        size=pygame.Vector2(150,150),
        speed=150,
        pos=pos,
        direction=getDirection(pos, (screenWidth/2,screenHeight/2)),
        lifetime=20,
        spread=20,
        onHit=onHit,
        damage=damage,
    )
    Global.msAttackGroup.add(newBanana)
    def drop():
        if newBanana.alive():
            newBananaPeel = BananaPeel(
                size=pygame.Vector2(120,120),
                speed=150,
                pos=newBanana.pos,
                lifetime=8,
                onHit=onHit,
                damage=damage,
            )
            Global.msAttackGroup.add(newBananaPeel)
            newBanana.kill()

    Timer(random.uniform(1,8), drop, Global.timerGroup)

class Banana(pygame.sprite.Sprite):
    def __init__(
        self,
        size: pygame.Vector2,
        speed: pygame.Vector2,
        pos: pygame.Vector2,
        direction,
        lifetime: float,
        spread: int,
        onHit,
        damage,
    ):
        super().__init__()
        self.size = size
        self.speed = speed
        self.angle = 90
        self.direction = direction.rotate(random.uniform(-spread, spread))
        self.pos = pos
        self.lifetime = lifetime
        self._lastAngle = None
        self.onHit = onHit
        self.type = "EnemyProjectile"

        self.ogImage = Global.loadImage("Assets/Projectiles/Banana.png", (int(size.x), int(size.y)))
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                Global.playerSprite.takeDamage(damage)
                if self.onHit:
                    self.onHit()
                self.kill()
        self.hitbox = Global.hitbox.new(
            pos=pos + pygame.Vector2(Global.minesweeperBox.rect.x,Global.minesweeperBox.rect.y),
            size=pygame.Vector2(65,65),
            hitFunction=hit,
            lifetime=lifetime,
            visualize=False,
            owner=self,
        )

        self.particleCD1 = 0

    def update(self):
        offsetPos = self.pos + pygame.Vector2(Global.minesweeperBox.rect.x,Global.minesweeperBox.rect.y)

        self.pos += self.direction * self.speed * Global.dt

        self.angle += self.speed * Global.dt * 2
        roundedAngle = round(self.angle / 2) * 2
        if roundedAngle != self._lastAngle:
            self._lastAngle = roundedAngle
            center = self.rect.center
            self.image = pygame.transform.rotate(self.ogImage, roundedAngle)
            self.rect = self.image.get_rect(center=center)

        self.rect.center = self.pos
        self.hitbox.pos = offsetPos

        self.lifetime -= Global.dt
        if self.lifetime <= 0:
            self.kill()

        if (
            self.pos[0] < -50 or
            self.pos[0] > Global.minesweeperSurfaceSize.x + 50 or
            self.pos[1] < -50 or
            self.pos[1] > Global.minesweeperSurfaceSize.y + 50
        ):
            self.kill()

        self.particleCD1 -= Global.dt
        if self.particleCD1 <= 0:
            self.particleCD1 = 0.05
            particlePos = self.pos[0] + random.randint(-35, 35), self.pos[1] + random.randint(-35, 35)
            Particle(
                groups=Global.msParticleGroup, 
                pos=particlePos, 
                color=(204, 102, 0), 
                direction=-self.direction, 
                speed=random.randint(80, 150),
                size=25,
                fadeSpeed=1000,
            )

    def kill(self):
        if hasattr(self, "hitbox"):
            self.hitbox.kill()
        super().kill()

class BananaPeel(pygame.sprite.Sprite):
    def __init__(
        self,
        size: pygame.Vector2,
        speed: pygame.Vector2,
        pos: pygame.Vector2,
        lifetime: float,
        onHit,
        damage,
    ):
        super().__init__()
        self.size = size
        self.speed = speed
        self.angle = 90
        self.pos = pos
        self.lifetime = lifetime
        self._lastAngle = None
        self.onHit = onHit
        self.type = "EnemyProjectile"

        self.ogImage = Global.loadImage("Assets/Projectiles/BananaPeel.png", (int(size.x), int(size.y)))
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                Global.playerSprite.takeDamage(damage)
                if self.onHit:
                    self.onHit()
                self.kill()
        self.hitbox = Global.hitbox.new(
            pos=pos + pygame.Vector2(Global.minesweeperBox.rect.x,Global.minesweeperBox.rect.y),
            size=pygame.Vector2(55,55),
            hitFunction=hit,
            lifetime=lifetime,
            visualize=False,
            owner=self,
        )

        self.particleCD1 = 0

    def update(self):
        offsetPos = self.pos + pygame.Vector2(Global.minesweeperBox.rect.x,Global.minesweeperBox.rect.y)

        self.rect.center = self.pos
        self.hitbox.pos = offsetPos

        self.lifetime -= Global.dt
        if self.lifetime <= 0:
            self.kill()

        if (
            self.pos[0] < -50 or
            self.pos[0] > Global.minesweeperSurfaceSize.x + 50 or
            self.pos[1] < -50 or
            self.pos[1] > Global.minesweeperSurfaceSize.y + 50
        ):
            self.kill()

    def kill(self):
        if hasattr(self, "hitbox"):
            self.hitbox.kill()
        super().kill()

        