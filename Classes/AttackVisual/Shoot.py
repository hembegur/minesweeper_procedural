import pygame, Global

class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        size,
        ogPos,
        targetPos,
        speed,
        onArrive = None,
    ):
        super().__init__()
        self.size = size
        self.ogImage = Global.loadImage("Assets/Projectiles/Bullet.png", (int(size.x), int(size.y)))
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=ogPos)
        self.pos = ogPos.copy()
        self._target = targetPos.copy()
        self._moveSpeed = speed
        self._onArrive = onArrive
        
    def update(self):
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
            self.rect.center = self.pos