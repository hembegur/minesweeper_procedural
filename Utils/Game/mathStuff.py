import pygame, random

def getDirection(fromPos, toPos):
    direction = pygame.Vector2(toPos) - pygame.Vector2(fromPos)
    if direction.length() != 0:
        direction = direction.normalize()
    return direction

def getAngle(fromPos, toPos):
    direction = pygame.Vector2(toPos) - pygame.Vector2(fromPos)
    if direction.length() == 0:
        return 0
    return pygame.Vector2(1, 0).angle_to(direction)

def randomEdgePos(width, height):
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        return (random.randint(0, width), 0)
    elif side == "bottom":
        return (random.randint(0, width), height)
    elif side == "left":
        return (0, random.randint(0, height))
    else:  # right
        return (width, random.randint(0, height))