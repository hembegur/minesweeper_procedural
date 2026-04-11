import pygame, Global, math, random
from Utils.UiComponents.TextLabel import TextLabel
from Utils.Game.Particle import Particle

class GameOver(pygame.sprite.Sprite):
    def __init__(self, groups, onDone=None, duration: float = 3.0):
        super().__init__(groups)
        w, h = Global.screenWidth, Global.screenHeight

        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 255))
        self.rect  = self.image.get_rect()

        self._timer  = duration
        self._onDone = onDone

        self.label = TextLabel(
            text="FAILED, REVERTING TO PREVIOUS ROUND!",
            pos=pygame.Vector2(w / 2, h / 2),
            font_size=60,
            color=(200, 0, 0),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(self.label)

    def update(self, screen=None):
        self._timer -= Global.dt
        if self._timer <= 0:
            self.label.kill()
            if self._onDone:
                self._onDone()
            self.kill()