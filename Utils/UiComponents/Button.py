import pygame
from typing import Tuple, Optional, Callable

RGBA = Tuple[int, int, int, int]

class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        # background
        color: RGBA = (50, 50, 50, 255),
        hoverColor: RGBA = (80, 80, 80, 255),
        clickColor: RGBA = (30, 30, 30, 255),
        # border
        border: bool = False,
        borderColor: RGBA = (255, 255, 255, 255),
        borderWidth: int = 2,
        borderRadius: int = 0,
        # callback
        onClick: Optional[Callable] = None,
        # misc
        visible: bool = True,
        alpha: int = 255,
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups: g.add(self)
            else:
                groups.add(self)

        self.pos         = pygame.Vector2(pos)
        self.size        = pygame.Vector2(size)
        self.color       = color
        self.hoverColor  = hoverColor
        self.clickColor  = clickColor
        self.border      = border
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.onClick     = onClick
        self.visible     = visible
        self._alpha      = alpha

        self._hovered  = False
        self._clicked  = False

        w, h = int(self.size.x), int(self.size.y)
        self.image  = pygame.Surface((w, h), pygame.SRCALPHA)
        self.canvas = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect   = self.image.get_rect(topleft=self.pos)

        self._redraw()

    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _currentColor(self) -> RGBA:
        if self._clicked:  return self.clickColor
        if self._hovered:  return self.hoverColor
        return self.color

    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        w, h = int(self.size.x), int(self.size.y)
        r    = self.borderRadius

        rc, gc, bc = self._currentColor()[:3]
        baked = (rc, gc, bc, int(self._currentColor()[3] * self._alpha / 255))
        pygame.draw.rect(self.image, baked, (0, 0, w, h), border_radius=r)

        self.image.blit(self.canvas, (0, 0))

        if self.border:
            rb, gb, bb = self.borderColor[:3]
            baked_border = (rb, gb, bb, int(self.borderColor[3] * self._alpha / 255))
            pygame.draw.rect(self.image, baked_border, (0, 0, w, h),
                             width=self.borderWidth, border_radius=r)

    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setOnClick(self, fn: Callable):
        self.onClick = fn

    def setColor(self, color: RGBA = None, hoverColor: RGBA = None, clickColor: RGBA = None):
        if color      is not None: self.color      = color
        if hoverColor is not None: self.hoverColor = hoverColor
        if clickColor is not None: self.clickColor = clickColor

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos

    def setVisible(self, visible: bool):
        self.visible = visible

    # ──────────────────────────────────────────
    # Events
    # ──────────────────────────────────────────

    def handleEvent(self, event: pygame.event.Event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._clicked and self.rect.collidepoint(event.pos):
                if self.onClick:
                    self.onClick()
            self._clicked = False

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self, screen=None):
        if not self.visible:
            self.image.fill((0, 0, 0, 0))
            return

        self._hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self._redraw()