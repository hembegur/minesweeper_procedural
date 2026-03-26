# ui_group = pygame.sprite.Group()

# panel = Box(
#     pos=pygame.Vector2(100, 100),
#     size=pygame.Vector2(200, 120),
#     groups=ui_group,
#     color=(30, 30, 30, 200),
#     border=True,
#     borderColor=(255, 255, 255, 255),
#     borderWidth=2,
#     borderRadius=8,
#     shadow=True,
#     shadowColor=(0, 0, 0, 120),
#     shadowOffset=pygame.Vector2(4, 4),
# )

# # game loop
# ui_group.update(screen)  # pass screen so shadows can be drawn
# ui_group.draw(screen)
# panel.canvas is the surface to blits shit in
import pygame
from typing import Tuple, Optional

RGBA = Tuple[int, int, int, int]

class Box(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups: pygame.sprite.Group = None,
        # background
        color: RGBA = (50, 50, 50, 255),
        # border
        border: bool = False,
        borderColor: RGBA = (255, 255, 255, 255),
        borderWidth: int = 2,
        borderRadius: int = 0,
        # misc
        visible: bool = True,
        alpha: int = 255,
    ):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)

        self.color = color
        self.border = border
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius

        self.visible = visible
        self._alpha = alpha

        # required by pygame.sprite.Sprite
        w, h = int(self.size.x), int(self.size.y)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.canvas = pygame.Surface((w, h), pygame.SRCALPHA)
        self._redraw()
    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────        
    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        w, h = int(self.size.x), int(self.size.y)
        r = self.borderRadius

        rc, gc, bc = self.color[:3]
        baked_color = (rc, gc, bc, int(self.color[3] * self._alpha / 255))
        pygame.draw.rect(self.image, baked_color, (0, 0, w, h), border_radius=r)

        self.image.blit(self.canvas, (0, 0))

        if self.border:
            rb, gb, bb = self.borderColor[:3]
            baked_border = (rb, gb, bb, int(self.borderColor[3] * self._alpha / 255))
            pygame.draw.rect(
                self.image, baked_border,
                (0, 0, w, h),
                width=self.borderWidth,
                border_radius=r,
            )
    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setColor(self, color: RGBA):
        self.color = color
        self._redraw()

    def setAlpha(self, alpha: int):
        self._alpha = max(0, min(255, alpha))
        self._redraw()  # redraw with new alpha baked in, not set_alpha()

    def setBorder(self, enabled: bool, color: Optional[RGBA] = None,
                  width: Optional[int] = None, radius: Optional[int] = None):
        self.border = enabled
        if color  is not None: self.borderColor  = color
        if width  is not None: self.borderWidth  = width
        if radius is not None: self.borderRadius = radius
        self._redraw()

    def setShadow(self, enabled: bool, color: Optional[RGBA] = None,
                  offset: Optional[pygame.Vector2] = None):
        self.shadow = enabled
        if color  is not None: self.shadowColor  = color
        if offset is not None: self.shadowOffset = pygame.Vector2(offset)

    def setSize(self, size: pygame.Vector2):
        self.size = pygame.Vector2(size)
        old_topleft = self.rect.topleft if self.rect else self.pos
        self._build()
        self.rect.topleft = old_topleft

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos

    def setVisible(self, visible: bool):
        self.visible = visible

    def toggle(self, attr: str):
        if hasattr(self, attr) and isinstance(getattr(self, attr), bool):
            setattr(self, attr, not getattr(self, attr))
            self._redraw()

    # ──────────────────────────────────────────
    # Sprite update  (called by group.update())
    # ──────────────────────────────────────────

    def update(self, screen: Optional[pygame.Surface] = None):
        if not self.visible:
            self.image.fill((0, 0, 0, 0))  # draw nothing
            return

        self._redraw()
        