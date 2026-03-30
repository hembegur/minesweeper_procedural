import pygame
from typing import Tuple, Optional, List

RGBA = Tuple[int, int, int, int]

class ScrollBox(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        # background
        color: RGBA = (50, 50, 50, 255),
        # border
        border: bool = False,
        borderColor: RGBA = (255, 255, 255, 255),
        borderWidth: int = 2,
        borderRadius: int = 0,
        # layout
        padding: int = 10,
        spacing: int = 8,
        direction: str = "vertical",    # "vertical" or "horizontal"
        # scroll
        scrollSpeed: int = 20,
        scrollbar: bool = True,
        scrollbarColor: RGBA = (100, 100, 100, 255),
        scrollbarWidth: int = 6,
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

        self.pos           = pygame.Vector2(pos)
        self.size          = pygame.Vector2(size)
        self.color         = color
        self.border        = border
        self.borderColor   = borderColor
        self.borderWidth   = borderWidth
        self.borderRadius  = borderRadius
        self.padding       = padding
        self.spacing       = spacing
        self.direction     = direction
        self.scrollSpeed   = scrollSpeed
        self.scrollbar     = scrollbar
        self.scrollbarColor = scrollbarColor
        self.scrollbarWidth = scrollbarWidth
        self.visible       = visible
        self._alpha        = alpha

        self._items: List[pygame.Surface] = []   # list of (surface, rect) tuples
        self._scrollOffset = 0
        self._maxScroll    = 0

        w, h = int(self.size.x), int(self.size.y)
        self.image  = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect   = self.image.get_rect(topleft=self.pos)
        self.canvas = pygame.Surface((w, h), pygame.SRCALPHA)

        self._redraw()

    # ──────────────────────────────────────────
    # Items
    # ──────────────────────────────────────────

    def addItem(self, item):
        """Add a surface or sprite as an item."""
        self._items.append(item)
        self._repositionItems()
        return len(self._items) - 1

    def removeItem(self, index: int):
        """Remove item by index."""
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._repositionItems()

    def clearItems(self):
        self._items.clear()
        self._scrollOffset = 0
        self._maxScroll    = 0
        self._repositionItems()

    def _getSurface(self, item):
        if isinstance(item, pygame.sprite.Sprite):
            return item.image
        return item

    def _repositionItems(self):
        if not self._items:
            self._maxScroll = 0
            return
        total = self.padding
        for item in self._items:
            surf = self._getSurface(item)
            if self.direction == "vertical":
                total += surf.get_height() + self.spacing
            else:
                total += surf.get_width() + self.spacing
        total += self.padding
        if self.direction == "vertical":
            self._maxScroll = max(0, total - int(self.size.y))
        else:
            self._maxScroll = max(0, total - int(self.size.x))
        self._scrollOffset = min(self._scrollOffset, self._maxScroll)

    # ──────────────────────────────────────────
    # Scroll
    # ──────────────────────────────────────────

    def scroll(self, amount: int):
        """Positive = scroll down/right, negative = up/left."""
        self._scrollOffset = max(0, min(self._maxScroll, self._scrollOffset + amount))

    def scrollTo(self, offset: int):
        self._scrollOffset = max(0, min(self._maxScroll, offset))

    def scrollToTop(self):
        self._scrollOffset = 0

    def scrollToBottom(self):
        self._scrollOffset = self._maxScroll

    def handleScroll(self, event: pygame.event.Event):
        """Pass pygame events here to enable mouse wheel scrolling."""
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if self.direction == "vertical":
                    self.scroll(-event.y * self.scrollSpeed)
                else:
                    self.scroll(-event.y * self.scrollSpeed)

    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setColor(self, color: RGBA):
        self.color = color

    def setAlpha(self, alpha: int):
        self._alpha = max(0, min(255, alpha))

    def setBorder(self, enabled: bool, color: Optional[RGBA] = None,
                  width: Optional[int] = None, radius: Optional[int] = None):
        self.border = enabled
        if color  is not None: self.borderColor  = color
        if width  is not None: self.borderWidth  = width
        if radius is not None: self.borderRadius = radius

    def setScrollSpeed(self, speed: int):
        self.scrollSpeed = speed

    def setPadding(self, padding: int):
        self.padding = padding
        self._repositionItems()

    def setSpacing(self, spacing: int):
        self.spacing = spacing
        self._repositionItems()

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos

    def setVisible(self, visible: bool):
        self.visible = visible

    # ──────────────────────────────────────────
    # Draw
    # ──────────────────────────────────────────

    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        w, h = int(self.size.x), int(self.size.y)
        r    = self.borderRadius

        # background
        rc, gc, bc = self.color[:3]
        baked = (rc, gc, bc, int(self.color[3] * self._alpha / 255))
        pygame.draw.rect(self.image, baked, (0, 0, w, h), border_radius=r)

        # draw items onto canvas with scroll offset applied
        self.canvas.fill((0, 0, 0, 0))
        cursor = self.padding

        for item in self._items:
            surf = item.image if isinstance(item, pygame.sprite.Sprite) else item
            if self.direction == "vertical":
                y = cursor - self._scrollOffset
                if -surf.get_height() < y < h:
                    self.canvas.blit(surf, (self.padding, y))
                    # update sprite rect to match screen position
                    if isinstance(item, pygame.sprite.Sprite):
                        item.rect.topleft = (
                            self.rect.x + self.padding,
                            self.rect.y + y,
                        )
                else:
                    # off screen — move rect out of view so collide doesn't trigger
                    if isinstance(item, pygame.sprite.Sprite):
                        item.rect.topleft = (-1000, -1000)
                cursor += surf.get_height() + self.spacing
            else:
                x = cursor - self._scrollOffset
                if -surf.get_width() < x < w:
                    self.canvas.blit(surf, (x, self.padding))
                    if isinstance(item, pygame.sprite.Sprite):
                        item.rect.topleft = (
                            self.rect.x + x,
                            self.rect.y + self.padding,
                        )
                else:
                    if isinstance(item, pygame.sprite.Sprite):
                        item.rect.topleft = (-1000, -1000)
                cursor += surf.get_width() + self.spacing

        self.image.blit(self.canvas, (0, 0))

        # scrollbar
        if self.scrollbar and self._maxScroll > 0:
            if self.direction == "vertical":
                barH      = max(20, int(h * h / (h + self._maxScroll)))
                barY      = int((h - barH) * self._scrollOffset / self._maxScroll)
                barX      = w - self.scrollbarWidth - 4
                barRect   = pygame.Rect(barX, barY, self.scrollbarWidth, barH)
            else:
                barW      = max(20, int(w * w / (w + self._maxScroll)))
                barX      = int((w - barW) * self._scrollOffset / self._maxScroll)
                barY      = h - self.scrollbarWidth - 4
                barRect   = pygame.Rect(barX, barY, barW, self.scrollbarWidth)

            sr, sg, sb = self.scrollbarColor[:3]
            baked_bar  = (sr, sg, sb, int(self.scrollbarColor[3] * self._alpha / 255))
            pygame.draw.rect(self.image, baked_bar, barRect, border_radius=4)

        # border drawn last — always on top
        if self.border:
            rb, gb, bb = self.borderColor[:3]
            baked_border = (rb, gb, bb, int(self.borderColor[3] * self._alpha / 255))
            pygame.draw.rect(self.image, baked_border, (0, 0, w, h),
                             width=self.borderWidth, border_radius=r)

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self, screen=None):
        if not self.visible:
            self.image.fill((0, 0, 0, 0))
            return
        self._redraw()