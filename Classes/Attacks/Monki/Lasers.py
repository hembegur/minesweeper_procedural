import pygame, Global, random, math

def spawnLaser(
    surfaceSize: pygame.Vector2,
    groups,
    warningDuration: float = 1.5,
    warningColor: tuple = (255, 50, 50),
    laserColor: tuple = (255, 200, 50),
    laserWidth: int = 40,
    laserDuration: float = 0.5,
    damage: int = 1,
    onHit = None,
    axis: str = "horizontal",
    # stream settings
    stream: bool = False,
    streamCount: int = 3,
    streamSpacing: int = 100,    # pixels between each beam
    streamDelay: float = 0.2,    # seconds between each beam
):
    w, h = int(surfaceSize.x), int(surfaceSize.y)

    def _spawnSingle(offset: int):
        if axis == "horizontal":
            y    = max(0, min(h, offset))
            pos1 = pygame.Vector2(0, y)
            pos2 = pygame.Vector2(w, y)
        else:
            x    = max(0, min(w, offset))
            pos1 = pygame.Vector2(x, 0)
            pos2 = pygame.Vector2(x, h)

        warning = Laser(
            pos1=pos1,
            pos2=pos2,
            groups=groups,
            color=warningColor,
            width=10,
            alpha=180,
        )
        # copy image to avoid shared surface issue
        warning.image = warning.image.copy()

        def spawnReal():
            warning.kill()

            real = Laser(
                pos1=pos1,
                pos2=pos2,
                groups=groups,
                color=laserColor,
                width=laserWidth,
                alpha=255,
            )

            delta  = pos2 - pos1
            length = max(1, int(delta.length()))
            center = pos1 + delta / 2
            hbSize = pygame.Vector2(length, laserWidth) if axis == "horizontal" else pygame.Vector2(laserWidth, length)

            def hit(otherHB):
                if otherHB.owner == pygame.mouse:
                    Global.playerSprite.takeDamage(damage)
                    if onHit:
                        onHit()

            real.hitbox = Global.hitbox.new(
                pos=center + pygame.Vector2(Global.minesweeperBox.rect.x, Global.minesweeperBox.rect.y),
                size=hbSize,
                hitFunction=hit,
                lifetime=0.2,
                visualize=False,
                owner=real,
            )

            real.shrinkAndFade(
                targetWidth=0,
                shrinkSpeed=laserWidth / laserDuration,
                targetAlpha=0,
                fadeSpeed=255 / laserDuration,
                onDone=real.kill,
            )

        _Timer(warningDuration, spawnReal, Global.timerGroup)

    if not stream:
        # single laser at random position
        offset = random.randint(0, h if axis == "horizontal" else w)
        _spawnSingle(offset)
    else:
        # stream of lasers with spacing and delay between each
        startOffset = random.randint(0, (h if axis == "horizontal" else w) - streamSpacing * streamCount)
        for i in range(streamCount):
            offset = startOffset + i * streamSpacing
            _Timer(i * streamDelay, lambda o=offset: _spawnSingle(o), Global.timerGroup)


class _Timer(pygame.sprite.Sprite):
    """Internal helper — calls onDone after delay then kills itself."""
    def __init__(self, delay: float, onDone, groups):
        super().__init__(groups)
        self.image   = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect    = self.image.get_rect()
        self._t      = delay
        self._onDone = onDone

    def update(self, dt: float = None):
        dt = dt or Global.dt
        self._t -= dt
        if self._t <= 0:
            self._onDone()
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        pos1: pygame.Vector2,
        pos2: pygame.Vector2,
        groups,
        color: tuple = (255, 50, 50, 255),
        width: int = 10,
        alpha: int = 255,
    ):
        super().__init__(groups)
        self.pos1   = pygame.Vector2(pos1)
        self.pos2   = pygame.Vector2(pos2)
        self.color  = color
        self.width  = width
        self.alpha  = alpha

        self._shrinkSpeed = 0
        self._shrinkTo    = 0
        self._fadeSpeed   = 0
        self._fadeTo      = 0
        self._onDone      = None

        self._build()
    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _build(self):
        delta   = self.pos2 - self.pos1
        length  = max(1, int(delta.length()))
        angle   = math.degrees(math.atan2(-delta.y, delta.x))
        w       = max(1, int(self.width))

        # surface is length x width, drawn as horizontal line then rotated
        surf = pygame.Surface((length, w), pygame.SRCALPHA)
        r, g, b = self.color[:3]
        surf.fill((r, g, b, int(self.alpha)))

        self.image = pygame.transform.rotate(surf, angle)
        self.rect  = self.image.get_rect(center=self.pos1 + delta / 2)

    # ──────────────────────────────────────────
    # Controls
    # ──────────────────────────────────────────

    def shrinkTo(self, targetWidth: float, speed: float):
        """Smoothly reduce width to targetWidth at speed (px/sec)."""
        self._shrinkSpeed = speed
        self._shrinkTo    = targetWidth

    def fadeTo(self, targetAlpha: float, speed: float):
        """Smoothly reduce alpha to targetAlpha at speed (units/sec)."""
        self._fadeSpeed = speed
        self._fadeTo    = targetAlpha

    def shrinkAndFade(self, targetWidth: float, shrinkSpeed: float,
                      targetAlpha: float, fadeSpeed: float, onDone=None):
        """Convenience — shrink and fade simultaneously."""
        self.shrinkTo(targetWidth, shrinkSpeed)
        self.fadeTo(targetAlpha, fadeSpeed)
        self._onDone = onDone

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self, dt: float = None):
        dt = dt or Global.dt
        dirty = False

        # shrink
        if self._shrinkSpeed > 0:
            diff = self.width - self._shrinkTo
            step = self._shrinkSpeed * dt
            if diff <= step:
                self.width = self._shrinkTo
                self._shrinkSpeed = 0
            else:
                self.width -= step
            dirty = True

        # fade
        if self._fadeSpeed > 0:
            diff = self.alpha - self._fadeTo
            step = self._fadeSpeed * dt
            if diff <= step:
                self.alpha = self._fadeTo
                self._fadeSpeed = 0
            else:
                self.alpha -= step
            dirty = True

        # check done
        if self._shrinkSpeed == 0 and self._fadeSpeed == 0 and self._onDone:
            self._onDone()
            self._onDone = None

        if dirty:
            self._build()

        