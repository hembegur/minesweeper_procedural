import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Services.mapService import map_all_tiles, map_destroy

def deflect():
    pos = pygame.mouse.get_pos()
    boxOffset = pygame.Vector2(Global.minesweeperBox.rect.topleft)
    particlePos = pos - boxOffset 
    Particle(
        groups=Global.msParticleGroup, 
        pos=particlePos, 
        color=(117, 241, 255), 
        direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                    math.sin(random.uniform(0, 2 * math.pi))), 
        speed=0,
        size=500,
        fadeSpeed=100,
    )
    def hit(otherHB):
        if hasattr(otherHB.owner, "type"):
            if otherHB.owner.type == "EnemyProjectile":
                #print("yes")
                otherHB.owner.kill()
    Global.hitbox.new(
        pos=pygame.Vector2(pos),
        size=pygame.Vector2(400,400),
        hitFunction=hit,
        lifetime=2,
        visualize=False,
        owner=None,
    )
        