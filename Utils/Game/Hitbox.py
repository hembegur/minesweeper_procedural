import pygame, Global

collisionGroupsCanCollide = {
    "Default": ["Default"],
    "Player": [""]
}

class hitbox(pygame.sprite.Sprite):
    def __init__(
            self, 
            pos:pygame.Vector2, 
            size:pygame.Vector2, 
            hitFunction,
            lifetime=None, 
            visualize=False, 
            collisionGroup="Default",
        ):
        super().__init__()
        self.rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        self.visualize = visualize
        self.lifetime = lifetime
        self.collisionGroup = collisionGroup
        self.hitFunction = hitFunction
        self.alreadyHit = set()

        # visualization surface
        self.surface = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 128))

        self.image = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 0))

    def update(self, pos=None):
        if pos is not None:
            self.rect.topleft = pos

        if self.visualize:
            Global.screen.blit(self.surface, self.rect.topleft)

        if self.lifetime is not None:
            self.lifetime -= Global.dt
            if self.lifetime <= 0:
                self.kill()

    def isAlive(self):
        return self.lifetime is None or self.lifetime > 0

    def collide(self, other):
        for group in collisionGroupsCanCollide[self.collisionGroup]:
            if other.collisionGroup == group:
                return self.rect.colliderect(other.rect)
        return False
        

class Hitbox:
    def __init__(self):
        self.hitboxGroup = pygame.sprite.Group()

    def new(self, *args, **kwargs):
        newHB = hitbox(*args, **kwargs)
        self.hitboxGroup.add(newHB)
        return newHB
    
    def update(self):
        self.hitboxGroup.draw(Global.screen)
        self.hitboxGroup.update()

        #Collision
        collisions = pygame.sprite.groupcollide(
            self.hitboxGroup,
            self.hitboxGroup,
            False,
            False
        )

        checked = set()
        for hb, others in collisions.items():
            for other in others:
                if hb is other:
                    continue

                pair = tuple(sorted((id(hb), id(other))))
                if pair in checked:
                    continue
                checked.add(pair)

                if hb.collide(other) and other not in hb.alreadyHit:
                    hb.hitFunction()
                    hb.alreadyHit.add(other)
                    other.alreadyHit.add(hb)