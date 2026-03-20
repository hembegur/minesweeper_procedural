# from Utils.Game.Jiggle import Jiggle

# # attach to any sprite
# jiggle = Jiggle(
#     sprite=mySprite,
#     intensity=0.3,   # how extreme the stretch is (0.1 subtle → 0.5 crazy)
#     speed=10.0,      # cycles per second
#     axis="both",     # "x", "y", or "both" for squash & stretch
# )

# # trigger it once (e.g. on hit, on click)
# jiggle.play()

# # or loop forever (e.g. idle animation)
# jiggle.play(loop=True)

# # in your game loop
# jiggle.update(Global.dt)

# # stop early if needed
# jiggle.stop()

import pygame

class Jiggle:
    def __init__(
        self,
        sprite: pygame.sprite.Sprite,
        intensity: float = 0.2,
        speed: float = 8.0,
        axis: str = "both",   # "x", "y", or "both"
    ):
        self.sprite   = sprite
        self.intensity = intensity
        self.speed    = speed
        self.axis     = axis

        self._ogImage = sprite.image.copy()
        self._ogSize  = pygame.Vector2(sprite.image.get_size())
        self._t       = 0.0
        self._playing = False
        self._loop    = False

    # ──────────────────────────────────────────
    # Control
    # ──────────────────────────────────────────

    def play(self, loop: bool = False):
        """Start the jiggle animation."""
        self._ogImage = self.sprite.image.copy()   # snapshot current image
        self._ogSize  = pygame.Vector2(self.sprite.image.get_size())
        self._t       = 0.0
        self._playing = True
        self._loop    = loop

    def stop(self):
        """Stop and restore original image."""
        self._playing = False
        self._t       = 0.0
        self._restore()

    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _restore(self):
        center = self.sprite.rect.center
        self.sprite.image = self._ogImage.copy()
        self.sprite.rect  = self.sprite.image.get_rect(center=center)

    def _sineScale(self):
        """
        Returns (scaleX, scaleY).
        Width grows while height shrinks and vice-versa — squash & stretch.
        """
        import math
        wave = math.sin(self._t * self.speed)   # -1 → 1

        if self.axis == "x":
            sx = 1.0 + wave * self.intensity
            sy = 1.0
        elif self.axis == "y":
            sx = 1.0
            sy = 1.0 + wave * self.intensity
        else:                                   # "both" — squash & stretch
            sx = 1.0 + wave * self.intensity
            sy = 1.0 - wave * self.intensity * 0.5

        return sx, sy

    # ──────────────────────────────────────────
    # Update  (call every frame)
    # ──────────────────────────────────────────

    def update(self, dt: float):
        import math
        if not self._playing:
            return

        self._t += dt

        # one full cycle = 2π / speed  seconds
        cycle = (2 * math.pi) / self.speed
        if self._t >= cycle:
            if self._loop:
                self._t -= cycle
            else:
                self.stop()
                return

        sx, sy = self._sineScale()
        newW = max(1, int(self._ogSize.x * sx))
        newH = max(1, int(self._ogSize.y * sy))

        center = self.sprite.rect.center
        self.sprite.image = pygame.transform.scale(self._ogImage, (newW, newH))
        self.sprite.rect  = self.sprite.image.get_rect(center=center)