import pygame, Global, random

class Pointer(pygame.sprite.Sprite):
    def __init__(
        self,
        size: pygame.Vector2,
        speed: pygame.Vector2,
        pos: pygame.Vector2,
        layer: int = 1,
        group: pygame.sprite.Group = None,
        lifetime: float = None,
    ):
        super().__init__()
        group.add(self, layer = layer)
        self.size = size
        self.speed = speed
        self.angle = 90
        self.pos = pos
        self.lifetime = lifetime
        self._lastAngle = None
        self.onHit = None
        self.type = "Pointer"

        self.ogImage = Global.loadImage("Assets/Cursor.png", (int(size.x), int(size.y)))
        self.image = self.ogImage
        self.rect = self.image.get_rect(center=pos)

    def update(self, shit=None):
        self.angle += self.speed * Global.dt
        roundedAngle = round(self.angle / 2) * 2
        if roundedAngle != self._lastAngle:
            self._lastAngle = roundedAngle
            center = self.rect.center
            self.image = pygame.transform.rotate(self.ogImage, roundedAngle)
            self.rect = self.image.get_rect(center=center)

        self.rect.center = self.pos

        if self.lifetime:
            self.lifetime -= Global.dt
            if self.lifetime <= 0:
                self.kill()
        