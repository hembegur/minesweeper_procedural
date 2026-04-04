import pygame, Global, random, math
from Utils.Game.mathStuff import randomEdgePos, getDirection, Timer
from Utils.Game.Particle import Particle, ImageParticle
from Utils.Game.mathStuff import getAngle

def spawnSpikePunch(damage: int = 10, spikeDamage: int = 5, onHit = None):
    def newPos():
        screenWidth  = random.randint(100, int(Global.minesweeperSurfaceSize.x)-100)
        screenHeight = random.randint(100, int(Global.minesweeperSurfaceSize.y)-100)
        return pygame.Vector2(screenWidth, screenHeight)
    pos1 = newPos()
    #pos2 = newPos()

    # ── 1. Warning sign ──
    warning = _WarningSign(
        pos=pos1,
        groups=Global.msAttackGroup,
    )

    # ── 2. After 1 second, spawn the punch ──
    def onWarningDone():
        warning.kill()
        _spawnPunch(pos1, damage, spikeDamage, onHit=onHit)

    Timer(1.0, onWarningDone, Global.timerGroup)


def _spawnPunch(pos, damage, spikeDamage, count=8, onHit=None):
    # punch image particle
    punch = ImageParticle(
        groups=Global.msAttackGroup,
        pos=pos,
        imagePath="Assets/Attacks/Punch.png",
        direction=pygame.Vector2(0,0),
        speed=0,
        size=200,
        fadeSpeed=150,
        shrinkSpeed=0,
        rotation=0,
    )

    # punch hitbox — moves with the particle
    def punchHit(otherHB):
        if otherHB.owner == pygame.mouse:
            Global.playerSprite.takeDamage(damage)
            punch.kill()
            if onHit:
                onHit()

    punch.hitbox = Global.hitbox.new(
        pos=pygame.Vector2(pos) + pygame.Vector2(Global.minesweeperBox.rect.x, Global.minesweeperBox.rect.y),
        size=pygame.Vector2(150,150),
        hitFunction=punchHit,
        lifetime=0.2,
        visualize=False,
        owner=punch,
    )

    # override punch update to move hitbox with it
    _origPunchUpdate = punch.update
    def _punchUpdate():
        _origPunchUpdate()
        if hasattr(punch, "hitbox"):
            punch.hitbox.pos = punch.pos + pygame.Vector2(
                Global.minesweeperBox.rect.x,
                Global.minesweeperBox.rect.y
            )
    punch.update = _punchUpdate

    # override punch kill to clean hitbox
    def _punchKill():
        if hasattr(punch, "hitbox"):
            punch.hitbox.kill()
    punch.kill = _punchKill

    # ── 3. Spawn 5 spikes in spread directions ──
    #baseAngle   = math.degrees(math.atan2(direction.y, direction.x))
    for i in range(count):
        angle = (360 / count) * i
        spikeDir = pygame.Vector2(
            math.cos(math.radians(angle)),
            -math.sin(math.radians(angle))
        )

        _SpikeShard(
            pos=pygame.Vector2(pos),
            direction=spikeDir,
            damage=spikeDamage,
        )


class _WarningSign(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos   = pygame.Vector2(pos)
        self.image = Global.loadImage("Assets/Attacks/Warning.png", (80, 80)).copy()
        self.rect  = self.image.get_rect(center=pos)
        self._t    = 0
        self._flash = 0.15   # flash every 0.15s
        self._flashTimer = 0
        self._visible = True

    def update(self):
        self._t           += Global.dt
        self._flashTimer  += Global.dt
        if self._flashTimer >= self._flash:
            self._flashTimer = 0
            self._visible = not self._visible
            self.image.set_alpha(255 if self._visible else 80)


class _SpikeShard(pygame.sprite.Sprite):
    def __init__(self, pos, direction, damage):
        super().__init__(Global.msAttackGroup)
        self.pos       = pygame.Vector2(pos)
        self.direction = direction
        self.speed     = 300
        self.lifetime  = 5
        self._lastAngle = None
        self.angle     = 0
        self.type = "EnemyProjectile"

        self.ogImage = Global.loadImage("Assets/Attacks/SmallSpike.png", (40,40))
        angle = pygame.Vector2(1, 0).angle_to(direction)  # adjust +180 if your spike faces left
        self.image = pygame.transform.rotate(self.ogImage, -angle)
        self.pos += self.direction * 65
        self.rect  = self.image.get_rect(center=pos)

        def hit(otherHB):
            if otherHB.owner == pygame.mouse:
                Global.playerSprite.takeDamage(damage)
                self.kill()

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

        self.particleCD -= Global.dt
        if self.particleCD <= 0:
            self.particleCD = 0.06
            Particle(
                groups=Global.msParticleGroup,
                pos=(self.pos.x + random.randint(-10,10), self.pos.y + random.randint(-10,10)),
                color=(120, 0, 180),
                direction=-self.direction,
                speed=0,
                size=8,
                fadeSpeed=1200,
            )

    def kill(self):
        if hasattr(self, "hitbox"):
            self.hitbox.kill()
        super().kill()