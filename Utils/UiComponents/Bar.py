import pygame
from typing import Tuple, Optional

RGBA = Tuple[int, int, int, int]

class Bar(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        # values
        value: float = 100,
        maxValue: float = 100,
        minValue: float = 0,
        # colors
        fillColor: RGBA = (50, 200, 50, 255),
        emptyColor: RGBA = (60, 60, 60, 255),
        # border
        border: bool = True,
        borderColor: RGBA = (30, 30, 30, 255),
        borderWidth: int = 2,
        borderRadius: int = 0,
        # fill direction
        direction: str = "left",    # "left", "right", "up", "down"
        # misc
        visible: bool = True,
        alpha: int = 255,
        # smooth fill
        smooth: bool = False,
        smoothSpeed: float = 200,
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups: g.add(self)
            else:
                groups.add(self)

        self.pos         = pygame.Vector2(pos)
        self.size        = pygame.Vector2(size)
        self.value       = float(value)
        self.maxValue    = float(maxValue)
        self.minValue    = float(minValue)
        self.fillColor   = fillColor
        self.emptyColor  = emptyColor
        self.border      = border
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.direction   = direction
        self.visible     = visible
        self._alpha      = alpha
        self.smooth      = smooth
        self.smoothSpeed = smoothSpeed

        # smooth fill tracks the visual value separately
        self._displayValue = float(value)

        w, h = int(self.size.x), int(self.size.y)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=self.pos)

        self._redraw()

    # Internal
    def _fillRatio(self) -> float:
        span = self.maxValue - self.minValue
        if span == 0:
            return 0
        return max(0.0, min(1.0, (self._displayValue - self.minValue) / span))

    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        w, h   = int(self.size.x), int(self.size.y)
        r      = self.borderRadius
        ratio  = self._fillRatio()

        # bake alpha
        def bake(color):
            return (*color[:3], int(color[3] * self._alpha / 255))

        # background (empty)
        pygame.draw.rect(self.image, bake(self.emptyColor), (0, 0, w, h), border_radius=r)

        # fill rect based on direction
        if self.direction == "left":
            fillW = int(w * ratio)
            fillRect = pygame.Rect(0, 0, fillW, h)
        elif self.direction == "right":
            fillW = int(w * ratio)
            fillRect = pygame.Rect(w - fillW, 0, fillW, h)
        elif self.direction == "up":
            fillH = int(h * ratio)
            fillRect = pygame.Rect(0, 0, w, fillH)
        elif self.direction == "down":
            fillH = int(h * ratio)
            fillRect = pygame.Rect(0, h - fillH, w, fillH)

        if ratio > 0:
            # clip fill to border radius
            fill_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(fill_surf, bake(self.fillColor), fillRect, border_radius=r)
            self.image.blit(fill_surf, (0, 0))

        # border on top
        if self.border:
            pygame.draw.rect(self.image, bake(self.borderColor), (0, 0, w, h),
                             width=self.borderWidth, border_radius=r)

    # Setters
    def setValue(self, value: float):
        self.value = max(self.minValue, min(self.maxValue, value))
        if not self.smooth:
            self._displayValue = self.value

    def setMax(self, maxValue: float):
        self.maxValue = maxValue

    def setMin(self, minValue: float):
        self.minValue = minValue

    def setFillColor(self, color: RGBA):
        self.fillColor = color

    def setEmptyColor(self, color: RGBA):
        self.emptyColor = color

    def setBorder(self, enabled: bool, color: Optional[RGBA] = None,
                  width: Optional[int] = None, radius: Optional[int] = None):
        self.border = enabled
        if color  is not None: self.borderColor  = color
        if width  is not None: self.borderWidth  = width
        if radius is not None: self.borderRadius = radius

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos

    def setVisible(self, visible: bool):
        self.visible = visible

    def setAlpha(self, alpha: int):
        self._alpha = max(0, min(255, alpha))

    # Convenience
    def increase(self, amount: float):
        self.setValue(self.value + amount)

    def decrease(self, amount: float):
        self.setValue(self.value - amount)

    def isEmpty(self) -> bool:
        return self.value <= self.minValue

    def isFull(self) -> bool:
        return self.value >= self.maxValue

    def getPercent(self) -> float:
        return self._fillRatio() * 100

    # Update
    def kill(self):
        if getattr(self, "_killing", False):
            return
        self._killing = True
        super().kill()

    def update(self, screen=None):
        if not self.visible:
            self.image.fill((0, 0, 0, 0))
            return

        if self.smooth:
            import Global
            diff = self.value - self._displayValue
            step = self.smoothSpeed * Global.dt
            if abs(diff) <= step:
                self._displayValue = self.value
            else:
                self._displayValue += step if diff > 0 else -step

        self._redraw()