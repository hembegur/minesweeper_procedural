import pygame, Global, random
from Utils.Game.mathStuff import randomEdgePos, getDirection
from Utils.Game.Particle import Particle
from Utils.Game.mathStuff import Timer

def shootMinigun(onHit, damage, bulletCount, initialDelay=0.5, minDelay=0.1):
    screenWidth  = int(Global.minesweeperSurfaceSize.x)
    screenHeight = int(Global.minesweeperSurfaceSize.y)
    pos = randomEdgePos(screenWidth, screenHeight)

    shotsLeft = [bulletCount]
    delay     = [initialDelay]

    def shootNext():
        if shotsLeft[0] <= 0:
            return

        newBullet = bullet(
            speed=300,
            pos=pos,
            direction=getDirection(pos, (screenWidth/2, screenHeight/2)),
            lifetime=10,
            spread=40,
            onHit=onHit,
            damage=damage,
        )
        Global.msAttackGroup.add(newBullet)
        shotsLeft[0] -= 1

        if shotsLeft[0] > 0:
            # reduce delay each shot, clamp to minDelay
            delay[0] = max(minDelay, delay[0] * 0.75)
            Timer(delay[0], shootNext, Global.timerGroup)

    Timer(delay[0], shootNext, Global.timerGroup)

class bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, damage, spread, onHit, lifetime, speed):
        super().__init__(Global.msAttackGroup)
        self.pos       = pygame.Vector2(pos)
        self.direction = direction.rotate(random.uniform(-spread, spread))
        self.speed     = speed
        self.lifetime  = lifetime
        self.angle     = 0
        self.onHit = onHit

        self.ogImage = Global.loadImage("Assets/Projectiles/minigunShot.png", (40, 40))
        angle = pygame.Vector2(1, 0).angle_to(direction)
        self.image = pygame.transform.rotate(self.ogImage, -angle)
        self.rect  = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                Global.playerSprite.takeDamage(damage)
                self.kill()
                if self.onHit:
                    self.onHit()

        self.hitbox = Global.hitbox.new(
            pos=self.pos + pygame.Vector2(Global.minesweeperBox.rect.x, Global.minesweeperBox.rect.y),
            size=pygame.Vector2(20,20),
            hitFunction=hit,
            lifetime=self.lifetime,
            visualize=False,
            owner=self,
        )

        self.particleCD = 0

    def update(self):
        self.pos += self.direction * self.speed * Global.dt
        self.rect.center = self.pos
        self.hitbox.pos  = self.pos + pygame.Vector2(
            Global.minesweeperBox.rect.x,
            Global.minesweeperBox.rect.y
        )

        self.lifetime -= Global.dt
        if self.lifetime <= 0:
            self.kill()

        if (
            self.pos.x < -50 or self.pos.x > Global.minesweeperSurfaceSize.x + 50 or
            self.pos.y < -50 or self.pos.y > Global.minesweeperSurfaceSize.y + 50
        ):
            self.kill()

    def kill(self):
        if hasattr(self, "hitbox"):
            self.hitbox.kill()
        super().kill()

        