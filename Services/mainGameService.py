import pygame, Global, random
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.Box import Box

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        imagePath: str = None,
        color: tuple = (255, 255, 255, 255),
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups:
                    g.add(self)
            else:
                groups.add(self)

        self.pos  = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)

        if imagePath:
            raw        = Global.loadImage(imagePath, (int(size.x), int(size.y)))
            self.image = raw.copy()
        else:
            self.image = pygame.Surface((int(size.x), int(size.y)), pygame.SRCALPHA)
            self.image.fill(color)

        self.rect = self.image.get_rect(center=self.pos)

    def move(self, direction: pygame.Vector2, speed: float, dt: float = None):
        dt = dt or Global.dt
        if direction.length() == 0:
            return
        self.pos += direction.normalize() * speed * dt
        self.rect.center = self.pos

    def moveTo(self, destination: pygame.Vector2, speed: float, dt: float = None):
        dt    = dt or Global.dt
        delta = pygame.Vector2(destination) - self.pos
        dist  = delta.length()
        step  = speed * dt
        if dist <= step:
            self.pos = pygame.Vector2(destination)
        else:
            self.pos += delta.normalize() * step
        self.rect.center = self.pos

    def setPos(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

    def update(self):
        self.move(pygame.Vector2(-1, 0), speed=200)
        if (
            self.pos[0] < -100 or
            self.pos[0] > Global.mainGameBox.size.x + 100 or
            self.pos[1] < -100 or
            self.pos[1] > Global.mainGameBox.size.y + 100
        ):
            self.kill()
       # Global.mainGameBox.canvas.blit(self.image, self.rect)

class mainGameService:
    def __init__(self):
        self.spawnCD = (0.5,2)
        self.currentSpawn = 0 
        self.dt = Global.dt

    def stop(self,stop: bool):
        if stop:
            self.dt = 0
    
    def update(self):
        self.currentSpawn -= self.dt
        print(self.dt)
        if self.currentSpawn <= 0: 
            SimpleSprite(
                pos=pygame.Vector2(800, 100),
                size=pygame.Vector2(200,200),
                groups=Global.entityGroup,
                imagePath="Assets/Background/house1.png",
            )
            self.currentSpawn = random.uniform(self.spawnCD[0], self.spawnCD[1])