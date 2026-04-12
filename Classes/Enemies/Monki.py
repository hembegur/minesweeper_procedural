import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Classes.Attacks.Monki.Banana import spawnBanana
from Classes.Attacks.Monki.Punches import spawnSpikePunch
from Classes.Attacks.Monki.Lasers import spawnLaser
from Utils.UiComponents.Bar import Bar

class Monki(BaseEntity):
    def __init__(self, pos, size, groups):
        super().__init__(
            pos=pos,
            size=size,
            groups=groups,
            imagePath="Assets/Enemies/Monki.png",
            jiggleIntensity=0.05,
            jiggleSpeed=10.0,
            jiggleAxis="both",
        )
        self.stats = Global.getEnemyStats("Monki")
        self.name = "Monki"
        self.pos = pygame.Vector2(pos.x,-100)
        self.ogPos = pos.copy()
        self.hp = Global.enemyStats["Monki"]["HP"]
        self.maxHp = Global.enemyStats["Monki"]["HP"]
        self.playJiggle(loop=True)

        self.attackCD = Global.enemyStats["Monki"]["CD"]
        self.lastAttack = Global.enemyStats["Monki"]["CD"]
        self.team = "Enemy"

        self._target    = None
        self._moveSpeed = 300
        self._onArrive  = None

        self.moveTo(self.ogPos, 400)

        self.nameText = TextLabel(
            text=f"Monki ({self.hp} / {self.maxHp})",
            pos=pygame.Vector2(200,50),
            font_size=30,
            color=(50,50,50),
            font_name="Assets/Fonts/Rimouski.otf", 
            center=False,
        )
        Global.uiGroup.add(self.nameText)
        self.hpBar = Bar(
            pos=pygame.Vector2(75,85),
            size=pygame.Vector2(637.5, 10),
            groups=Global.uiGroup,
            value=100,
            maxValue=100,
            fillColor=(200, 50, 50, 255),
            emptyColor=(60, 60, 60, 255),
            border=False,
            smooth=True,
            smoothSpeed=150,
        )

    def takeDamage(self, amount):
        self.hp -= amount

    def attack(self):
        self.pos = pygame.Vector2(Global.playerSprite.pos)
        self.rect.center = self.pos
        self.moveTo(self.ogPos, 200)

        for _ in range(20):
            particlePos = self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.mainAttackGroup, 
                pos=particlePos, 
                color=(101, 9, 171), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(100, 250),
                size=random.randint(50, 90),
                fadeSpeed=500,
            )

    def moveTo(
        self,
        destination: pygame.Vector2,
        speed: float,
        onArrive=None,       # optional callback when destination reached
    ):
        self._target    = pygame.Vector2(destination)
        self._moveSpeed = speed
        self._onArrive  = onArrive

    def kill(self):
        self.hpBar.kill()
        self.nameText.kill()
        super().kill()

    def update(self):
        super().update()  # keeps jiggle running
        self.hpBar.setValue(self.hp / max(1, self.maxHp) * 100)
        self.nameText.setText(f"Monki ({f"{round(self.hp,1):g}HP"} / {self.maxHp})")

        if self.hp <= 0:
            self.kill()

        self.lastAttack -= Global.dt
        if self.lastAttack <= 0:
            choice = random.randint(1,4)
            if choice == 1:
                spawnSpikePunch(damage=Global.enemyStats["Monki"]["PunchDamage"], count=Global.enemyStats["Monki"]["PunchCount"], delay=0.1)
            elif choice == 2:
                spawnLaser(
                        surfaceSize=Global.minesweeperSurfaceSize,
                        groups=Global.msAttackGroup,
                        axis="horizontal",
                        stream=True,
                        streamCount=10,
                        streamSpacing=80,
                        streamDelay=0.4,
                        warningDuration=0.5,
                        laserWidth=100,
                        damage=Global.enemyStats["Monki"]["LaserDamage"],
                    )
                spawnLaser(
                        surfaceSize=Global.minesweeperSurfaceSize,
                        groups=Global.msAttackGroup,
                        axis="vertical",
                        stream=True,
                        streamCount=10,
                        streamSpacing=80,
                        streamDelay=0.4,
                        warningDuration=0.5,
                        laserWidth=100,
                        damage=Global.enemyStats["Monki"]["LaserDamage"],
                    )
            elif choice == 3:
                for _ in range(random.randint(5,15)):
                    spawnBanana(None, Global.enemyStats["Monki"]["BananaDamage"])
            elif choice == 4:
                for _ in range(random.randint(1,4)):
                    from Classes.Enemies.ClownEnemy import ClownEnemy
                    newEnemy = ClownEnemy(
                            pos=pygame.Vector2(random.randint(450, 650), random.randint(100, 450)),
                            size=pygame.Vector2(200, 200),
                            groups=Global.entityGroup,
                        )
                    Global.entityGroup.add(newEnemy)

            self.lastAttack = self.attackCD

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

            self.rect.center = self.pos