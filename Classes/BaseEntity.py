import pygame, Global
from typing import Tuple, Optional
from Utils.Game.Jiggle import Jiggle

RGBA = Tuple[int, int, int, int]

class BaseEntity(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups: pygame.sprite.Group = None,
        # image
        imagePath: Optional[str] = None,
        color: RGBA = (255, 255, 255, 255),
        # jiggle
        jiggleIntensity: float = 0.2,
        jiggleSpeed: float = 8.0,
        jiggleAxis: str = "both",
    ):
        super().__init__(groups) if groups else super().__init__()
        self.name = None
        self.hp = 100
        self.maxHp = 100
        self.pos   = pygame.Vector2(pos)
        self.size  = pygame.Vector2(size)
        self.color = color
        self.team = None

        self._imagePath = imagePath
        self._build()

        # jiggle
        self._jiggle = Jiggle(
            sprite=self,
            intensity=jiggleIntensity,
            speed=jiggleSpeed,
            axis=jiggleAxis,
        )
        self._jiggling = False

        self.dieFunction = None

    # ──────────────────────────────────────────
    # Build
    # ──────────────────────────────────────────

    def _build(self):
        if self._imagePath:
            raw = pygame.image.load(self._imagePath).convert_alpha()
            self.image = pygame.transform.scale(raw, (int(self.size.x), int(self.size.y)))
        else:
            self.image = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA)
            self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos 

        # keep a clean copy for jiggle / scaling
        self._ogImage = self.image.copy()
        self._ogSize  = pygame.Vector2(self.size)

    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos

    def setCenter(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

    def setSize(self, size: pygame.Vector2):
        self.size = pygame.Vector2(size)
        self._build()
        # re-attach jiggle with new image
        self._jiggle._ogImage = self._ogImage.copy()
        self._jiggle._ogSize  = pygame.Vector2(self._ogSize)

    def setImage(self, imagePath: str):
        self._imagePath = imagePath
        self._build()
        self._jiggle._ogImage = self._ogImage.copy()
        self._jiggle._ogSize  = pygame.Vector2(self._ogSize)

    def setColor(self, color: RGBA):
        self.color = color
        if not self._imagePath:
            self.image.fill(self.color)
            self._ogImage = self.image.copy()

    def setAlpha(self, alpha: int):
        self.image.set_alpha(max(0, min(255, alpha)))

    # ──────────────────────────────────────────
    # Jiggle controls
    # ──────────────────────────────────────────

    def setJiggleIntensity(self, intensity: float):
        self._jiggle.intensity = intensity

    def setJiggleSpeed(self, speed: float):
        self._jiggle.speed = speed

    def setJiggleAxis(self, axis: str):
        self._jiggle.axis = axis   # "x", "y", or "both"

    def toggleJiggle(self, loop: bool = True):
        self._jiggling = not self._jiggling
        if self._jiggling:
            self._jiggle.play(loop=loop)
        else:
            self._jiggle.stop()

    def playJiggle(self, loop: bool = False):
        self._jiggling = True
        self._jiggle.play(loop=loop)

    def stopJiggle(self):
        self._jiggling = False
        self._jiggle.stop()

    # ──────────────────────────────────────────
    # Movement helpers
    # ──────────────────────────────────────────

    def move(self, direction: pygame.Vector2, speed: float, dt: float):
        self.pos += direction * speed * dt
        self.rect.topleft = self.pos

    def moveCenter(self, direction: pygame.Vector2, speed: float, dt: float):
        self.pos += direction * speed * dt
        self.rect.center = self.pos

    def kill(self):
        if self.dieFunction:
            self.dieFunction()
        super().kill()

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self):
        self._jiggle.update(Global.dt)