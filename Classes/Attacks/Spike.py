import pygame, Global, random
from Utils.Game.mathStuff import randomEdgePos, getDirection
from Utils.Game.Particle import Particle
    
def spawnSpike():
    screenWidth = int(Global.minesweeperSurfaceSize.x)
    screenHeight = int(Global.minesweeperSurfaceSize.y)
    pos = randomEdgePos(screenWidth,screenHeight)
    newSpike = Spike(
        size=pygame.Vector2(150,150),
        speed=random.randint(50,250),
        pos=pos,
        direction=getDirection(pos, (screenWidth/2,screenHeight/2)),
        lifetime=20,
        spread=20,
    )
    Global.attackGroup.add(newSpike)
    
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

        self.ogImage = pygame.image.load("Assets/Attacks/Spike.png").convert_alpha()
        self.ogImage = pygame.transform.scale(self.ogImage, size)
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                print("Got ya ass")
        self.hitbox = Global.hitbox.new(
            pos=pos + pygame.Vector2(Global.minesweeperRect.x,Global.minesweeperRect.y),
            size=pygame.Vector2(60,60),
            hitFunction=hit,
            lifetime=lifetime,
            visualize=False,
            owner=self,
        )

        self.particleCD1 = 0

    def update(self):
        offsetPos = self.pos + pygame.Vector2(Global.minesweeperRect.x,Global.minesweeperRect.y)

        self.pos += self.direction * self.speed * Global.dt
        self.angle = self.angle + self.speed * Global.dt
        self.image = pygame.transform.rotate(self.ogImage, self.angle)
        rot_rect = self.image.get_rect(center=self.rect.center)
        self.rect = rot_rect
        self.rect.center = self.pos
        self.hitbox.pos = offsetPos

        self.lifetime -= Global.dt
        if self.lifetime <= 0:
            self.kill()

        if (
            self.pos[0] < -50 or
            self.pos[0] > Global.minesweeperSurfaceSize.x + 50 or
            self.pos[1] < -50 or
            self.pos[1] > Global.minesweeperSurfaceSize.x + 50
        ):
            self.kill()

        self.particleCD1 -= Global.dt
        if self.particleCD1 <= 0:
            self.particleCD1 = 0.05
            particlePos = self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-20, 20)
            color = (50,50,50,255)
            direction = self.direction#pygame.math.Vector2(0, -1)
            speed = random.randint(50, 100)
            newParticel = Particle(
                groups=Global.particleGroup, 
                pos=particlePos, 
                color=color, 
                direction=direction, 
                speed=speed,
                size=20,
            )

        