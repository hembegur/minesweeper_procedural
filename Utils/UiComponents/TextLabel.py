import pygame, Global

class TextLabel(pygame.sprite.Sprite):
    def __init__(
        self,
        text,
        pos,
        font_size=24,
        color=(255, 255, 255),
        font_name=None,
        center=False,
        antialias=True,
        outline: int = 0,                    # outline thickness, 0 = no outline
        outlineColor=(0, 0, 0),
    ):
        super().__init__()
        self.text         = text
        self.pos          = pygame.Vector2(pos)
        self.color        = color
        self.center       = center
        self.antialias    = antialias
        self.outline      = outline
        self.outlineColor = outlineColor
        self._alpha       = 255

        self.font  = pygame.font.Font(font_name, font_size)
        self.image = None
        self.rect  = None
        self._render()

        # moveTo state
        self._target      = None
        self._moveSpeed   = 0
        self._onArrive    = None

        # fade state
        self._fadeSpeed   = 0
        self._fadeTo      = 255
        self._onFadeDone  = None

    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _render(self):
        base = self.font.render(self.text, self.antialias, self.color)

        if self.outline > 0:
            o = self.outline
            w, h = base.get_width() + o * 2, base.get_height() + o * 2
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)

            # render outline by blitting in all 8 directions
            outline_surf = self.font.render(self.text, self.antialias, self.outlineColor)
            for dx in range(-o, o + 1):
                for dy in range(-o, o + 1):
                    if dx == 0 and dy == 0:
                        continue
                    self.image.blit(outline_surf, (dx + o, dy + o))

            # blit main text on top
            self.image.blit(base, (o, o))
        else:
            self.image = base

        self.image = self.image.convert_alpha()
        self.image.set_alpha(int(self._alpha))
        self.rect  = self.image.get_rect()

        if self.center:
            self.rect.center = self.pos
        else:
            self.rect.topleft = self.pos

    # ──────────────────────────────────────────
    # Setters
    # ──────────────────────────────────────────

    def setText(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self._render()

    def setOutline(self, thickness: int, color=None):
        self.outline = thickness
        if color is not None:
            self.outlineColor = color
        self._render()

    def setColor(self, color):
        self.color = color
        self._render()

    def setPosition(self, pos):
        self.pos = pygame.Vector2(pos)
        self._render()

    def setAlpha(self, alpha: float):
        self._alpha = max(0.0, min(255.0, alpha))
        self.image.set_alpha(int(self._alpha))

    # ──────────────────────────────────────────
    # moveTo
    # ──────────────────────────────────────────

    def moveTo(
        self,
        destination: pygame.Vector2,
        speed: float,
        onArrive=None,       # optional callback when destination reached
    ):
        """Move label toward destination at given speed (px/sec)."""
        self._target    = pygame.Vector2(destination)
        self._moveSpeed = speed
        self._onArrive  = onArrive

    def stopMove(self):
        self._target   = None
        self._onArrive = None

    # ──────────────────────────────────────────
    # Fade
    # ──────────────────────────────────────────

    def fadeTo(
        self,
        targetAlpha: float,
        speed: float,
        onDone=None,         # optional callback when fade finishes
    ):
        """Fade alpha toward targetAlpha at given speed (units/sec)."""
        self._fadeTo      = max(0.0, min(255.0, targetAlpha))
        self._fadeSpeed   = speed
        self._onFadeDone  = onDone

    def fadeIn(self, speed: float, onDone=None):
        self.fadeTo(255, speed, onDone)

    def fadeOut(self, speed: float, onDone=None):
        self.fadeTo(0, speed, onDone)

    def stopFade(self):
        self._fadeSpeed  = 0
        self._onFadeDone = None

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    def update(self, surface):
        # ── movement ──
        if self._target is not None:
            delta = self._target - self.pos
            dist  = delta.length()
            step  = self._moveSpeed * Global.dt

            if dist <= step:
                # arrived
                self.pos = pygame.Vector2(self._target)
                self._target = None
                if self._onArrive:
                    self._onArrive()
            else:
                self.pos += delta.normalize() * step

            # update rect
            if self.center:
                self.rect.center = self.pos
            else:
                self.rect.topleft = self.pos

        # ── fade ──
        if self._fadeSpeed > 0:
            diff = self._fadeTo - self._alpha
            step = self._fadeSpeed * Global.dt

            if abs(diff) <= step:
                self._alpha    = self._fadeTo
                self._fadeSpeed = 0
                self.image.set_alpha(int(self._alpha))
                if self._onFadeDone:
                    self._onFadeDone()
            else:
                self._alpha += step if diff > 0 else -step
                self.image.set_alpha(int(self._alpha))