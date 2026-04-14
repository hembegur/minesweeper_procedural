import pygame, sys, Global, random
from Utils.UiComponents.Box import Box
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.ScrollBox import ScrollBox

class PlayerStatsBox(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        currSize = pygame.Vector2(1100, 1000)
        boxPos   = pygame.Vector2(1350 - currSize.x/2, 540 - currSize.y/2)

        self.hideBox = Box(
            pos=boxPos,
            size=currSize,
            groups=Global.uiGroup,
            color=(30, 30, 30, 255),
            border=False,
        )
        Global.uiGroup.add(self.hideBox)

        self.continueText = TextLabel(
            text=f"Click to continue",
            pos=pygame.Vector2(1350, 200),
            font_size=80,
            color=(200, 50, 50),
            font_name="Assets/Fonts/Rimouski.otf",
            center=True,
        )
        Global.uiGroup.add(self.continueText)

        # scroll box inside the hideBox
        scrollPadding = 40
        self.statsScroll = ScrollBox(
            pos=boxPos + pygame.Vector2(scrollPadding, 280),
            size=pygame.Vector2(currSize.x - scrollPadding * 2, currSize.y - 320),
            groups=Global.uiGroup,
            color=(50, 50, 50, 180),
            border=True,
            borderColor=(80, 80, 80, 255),
            borderWidth=2,
            borderRadius=4,
            padding=15,
            spacing=8,
            direction="vertical",
            scrollSpeed=25,
            scrollbar=True,
            scrollbarColor=(120, 120, 120, 255),
        )

        self._statLabels = []
        self._buildStats()

    def _buildStats(self):
        # clear old labels
        for label in self._statLabels:
            label.kill()
        self._statLabels.clear()
        self.statsScroll.clearItems()

        stat_display = [
            ("HP",                    f"{formatStat(Global.playerStats['HP'])} / {formatStat(Global.playerStats['MaxHP'])}",   (100, 220, 100)),
            ("MP",                    f"{formatStat(Global.playerStats['MP'])} / {formatStat(Global.playerStats['MaxMP'])}",   (100, 100, 220)),
            ("Ult",                   f"{Global.playerStats['Ult']} / {Global.playerStats['MaxUlt']}", (200, 100, 220)),
            ("Damage",         f"{Global.playerStats['NormalDamage']} + {Global.playerStatsMultiplier['NormalDamage']}%", (220, 180, 80)),
            ("Attack Speed",          f"{Global.playerStats['AttackSpeed']}",                       (220, 180, 80)),
            ("Burst Count",           str(Global.playerStats['Burst']),                                (220, 180, 80)),
            ("Burst Attack Speed",    f"{Global.playerStats['BurstAttackSpeed']}",                  (160, 140, 80)),
            ("Defense",    f"{Global.playerStats['Defense']}",                  (180, 180, 180)),
            ("HP Regen",    f"{Global.playerStats['HPRegen']}",                  (100, 220, 100)),
            ("Life Steal",    f"{Global.playerStats['LifeSteal']}",                  (220, 80,  80)),
            ("Aoe",    f"{Global.playerStats['Aoe']}",                  (220, 180, 80)),
            ("## Gain ##", None,                                   (180, 180, 180)),
            ("HP Gain",               f"+{Global.playerStatsGain['HP']}",     (100, 220, 100)),
            ("MP Gain",               f"+{Global.playerStatsGain['MP']}",     (100, 100, 220)),
            ("Ult Gain",              f"+{Global.playerStatsGain['Ult']}",    (200, 100, 220)),
            ("## Lose ##",   None,                                   (180, 180, 180)),
            ("HP Lose",               f"-{Global.playerStatsLose['HP']}",     (220, 80,  80)),
            ("MP Lose",               f"-{Global.playerStatsLose['MP']}",     (100, 100, 220)),
            ("Ult Lose",              f"-{Global.playerStatsLose['Ult']}",    (200, 100, 220)),
        ]

        scrollW = int(self.statsScroll.size.x) - self.statsScroll.padding * 2 - self.statsScroll.scrollbarWidth - 8

        for key, value, color in stat_display:
            if value is None:
                # section header
                text = key
                labelColor = color
            else:
                text = f"{key}:   {value}"
                labelColor = color

            label = TextLabel(
                text=text,
                pos=pygame.Vector2(0, 0),
                font_size=28 if value is None else 24,
                color=labelColor,
                font_name="Assets/Fonts/Rimouski.otf",
                center=False,
            )
            self._statLabels.append(label)
            self.statsScroll.addItem(label.image)

    def refresh(self):
        """Call this to update stats display."""
        self._buildStats()

    def handleScroll(self, event):
        self.statsScroll.handleScroll(event)
        
    def kill(self):
        self.hideBox.kill()
        self.continueText.kill()
        self.statsScroll.kill()
        for label in self._statLabels:
            label.kill()
        self._statLabels.clear()
        super().kill()

def formatStat(value):
        return f"{value:.1f}".rstrip('0').rstrip('.')