import pygame, Global, random, math
from Utils.Game.mathStuff import randomEdgePos, getDirection, Timer
from Utils.Game.Particle import Particle, ImageParticle
from Utils.Game.mathStuff import getAngle

def spawnSpikePunch(
    damage: int = 10,
    onHit = None,
    count: int = 1,          # how many punches to spawn
    delay: float = 0.5,      # delay between each punch
):
    def spawnOne(i):
        def newPos():
            screenWidth  = random.randint(100, int(Global.minesweeperSurfaceSize.x)-100)
            screenHeight = random.randint(100, int(Global.minesweeperSurfaceSize.y)-100)
            return pygame.Vector2(screenWidth, screenHeight)

        pos = newPos()

        warning = _WarningSign(pos=pos, groups=Global.msAttackGroup)

        def onWarningDone():
            Global.SoundManager.playSFX("Assets/Sounds/SoundEffect/punch.wav", 0.2)
            warning.kill()
            _spawnPunch(pos, damage, onHit=onHit)

        Timer(1.0, onWarningDone, Global.timerGroup)

    for i in range(count):
        Timer(i * delay, lambda i=i: spawnOne(i), Global.timerGroup)


def _spawnPunch(pos, damage, onHit=None):
    punch = ImageParticle(
        groups=Global.msAttackGroup,
        pos=pos,
        imagePath="Assets/Attacks/Punch.png",
        direction=pygame.Vector2(0, 0),
        speed=0,
        size=300,
        fadeSpeed=150,
        shrinkSpeed=0,
        rotation=0,
        lifetime=3.0,
    )

    def punchHit(otherHB):
        if otherHB.owner == pygame.mouse:
            Global.playerSprite.takeDamage(damage)
            punch.kill()
            if onHit:
                onHit()

    punch.hitbox = Global.hitbox.new(
        pos=pygame.Vector2(pos) + pygame.Vector2(Global.minesweeperBox.rect.x, Global.minesweeperBox.rect.y),
        size=pygame.Vector2(250, 250),
        hitFunction=punchHit,
        lifetime=0.2,
        visualize=False,
        owner=punch,
    )

    _origPunchUpdate = punch.update
    def _punchUpdate():
        _origPunchUpdate()
        if hasattr(punch, "hitbox"):
            punch.hitbox.pos = punch.pos + pygame.Vector2(
                Global.minesweeperBox.rect.x,
                Global.minesweeperBox.rect.y
            )
    punch.update = _punchUpdate

    def _punchKill():
        if hasattr(punch, "hitbox"):
            punch.hitbox.kill()
        ImageParticle.kill(punch)
    punch.kill = _punchKill


class _WarningSign(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos         = pygame.Vector2(pos)
        self.image       = Global.loadImage("Assets/Attacks/Warning.png", (80, 80)).copy()
        self.rect        = self.image.get_rect(center=pos)
        self._flashTimer = 0
        self._visible    = True

    def update(self):
        self._flashTimer += Global.dt
        if self._flashTimer >= 0.15:
            self._flashTimer = 0
            self._visible    = not self._visible
            self.image.set_alpha(255 if self._visible else 80)