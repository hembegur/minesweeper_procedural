import pygame, Global, random
from Utils.Game.mathStuff import randomEdgePos, getDirection
from Utils.Game.Particle import Particle

def spawnSpike():
    screenWidth = int(Global.minesweeperSurfaceSize.x)
    screenHeight = int(Global.minesweeperSurfaceSize.y)
    pos = randomEdgePos(screenWidth,screenHeight)
    newSpike = Spike(
        size=pygame.Vector2(150,150),
        speed=150,
        pos=pos,
        direction=getDirection(pos, (screenWidth/2,screenHeight/2)),
        lifetime=20,
        spread=20,
    )
    Global.msAttackGroup.add(newSpike)

class Spike(pygame.sprite.Sprite):
    def __init__(
        self,
        size: pygame.Vector2,
        speed: pygame.Vector2,
        pos: pygame.Vector2,
        direction,
        lifetime: float,
        spread: int,
    ):
        super().__init__()
        self.size = size
        self.speed = speed
        self.angle = 90
        self.direction = direction.rotate(random.uniform(-spread, spread))
        self.pos = pos
        self.lifetime = lifetime
        self._lastAngle = None

        self.ogImage = Global.loadImage("Assets/Attacks/Spike.png", (int(size.x), int(size.y)))
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                Global.playerHP -= 5
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

        self.pos += self.direction * self.speed * Global.dt

        self.angle += self.speed * Global.dt
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
            self.hitbox.kill()

        if (
            self.pos[0] < -50 or
            self.pos[0] > Global.minesweeperSurfaceSize.x + 50 or
            self.pos[1] < -50 or
            self.pos[1] > Global.minesweeperSurfaceSize.x + 50
        ):
            self.kill()
            self.hitbox.kill()

        self.particleCD1 -= Global.dt
        if self.particleCD1 <= 0:
            self.particleCD1 = 0.05
            particlePos = self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.msParticleGroup, 
                pos=particlePos, 
                color=(50,50,50), 
                direction=-self.direction, 
                speed=random.randint(80, 150),
                size=20,
                fadeSpeed=1000,
            )

        