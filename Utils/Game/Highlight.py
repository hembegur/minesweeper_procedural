import pygame
import Global

_glow_cache = {}

def _normalize(value):
    if isinstance(value, pygame.math.Vector2):
        return (int(value.x), int(value.y))
    return tuple(value)


def _get_surface(size, color):
    size = _normalize(size)
    color = _normalize(color)

    key = (size, color)

    if key not in _glow_cache:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(color)
        _glow_cache[key] = surface

    return _glow_cache[key]


def highlight(size, position, color, additive=False):
    surface = _get_surface(size, color)

    if isinstance(position, pygame.math.Vector2):
        position = (int(position.x), int(position.y))

    if additive:
        Global.screen.blit(surface, position, special_flags=pygame.BLEND_ADD)
    else:
        Global.screen.blit(surface, position)
