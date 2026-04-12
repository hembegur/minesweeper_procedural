import pygame, Global
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.Button import Button

class MainMenu:
    def __init__(self):
        w, h = Global.screenWidth, Global.screenHeight
        self.active = True
        self.sprites = []

        # background box
        boxSize = pygame.Vector2(2000,2000)
        boxPos  = pygame.Vector2(0,0)
        self.box = Box(
            pos=boxPos,
            size=boxSize,
            groups=None,
            color=(255, 255, 255, 255),
            border=False,
        )
        Global.uiGroup.add(self.box, layer = 10)

        # title
        self.title = TextLabel(
            text="Rouge Sweeper",
            pos=pygame.Vector2(w / 2, h / 2 - 120),
            font_size=180,
            color=(30, 30, 30),
            font_name="Assets/Fonts/Pixel.TTF",
            center=True,
        )
        Global.uiGroup.add(self.title, layer = 12)

        # start button
        btnSize = pygame.Vector2(400, 120)
        self.startBtn, self.startBtnText = self._buttonAndText(
            pos=pygame.Vector2(w / 2 - btnSize.x / 2, h / 2 + 40),
            size=btnSize,
            text="Start",
            onClick=self._onStart,
        )

        self.removed = False

    def _buttonAndText(self, pos, size, text, onClick):
        btn = Button(
            pos=pos,
            size=size,
            groups=None,
            color=(255,255,255, 255),
            hoverColor=(80, 80, 80, 255),
            clickColor=(20, 20, 20, 255),
            border=True,
            borderColor=(50,50,50, 255),
            borderRadius=15,
            borderWidth=8,
            onClick=onClick,
        )
        Global.uiGroup.add(btn, layer = 12)
        label = TextLabel(
            text=text,
            pos=pos + pygame.Vector2(size.x / 2, size.y / 2),
            font_size=80,
            color=(50,50,50),
            font_name="Assets/Fonts/Pixel.TTF",
            center=True,
        )
        Global.uiGroup.add(label, layer = 12)
        return btn, label

    def _onStart(self):
        self.remove()
        Global.gameState = "Preparing"

    def handleEvent(self, event):
        self.startBtn.handleEvent(event)

    def remove(self):
        self.active = False
        self.box.kill()
        self.title.kill()
        self.startBtn.kill()
        self.startBtnText.kill()
        self.removed = True