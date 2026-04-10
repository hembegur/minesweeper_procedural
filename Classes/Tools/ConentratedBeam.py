import pygame, Global, random, math
from Classes.BaseEntity import BaseEntity
from Utils.Game.Particle import Particle
from Utils.UiComponents.TextLabel import TextLabel
from Utils.Game.mathStuff import Timer

def concentrated_beam():
    target = Global.playerSprite.currentTarget
    if not target:
        return
    
    def shoot():
        if not target or target.hp <= 0:
            return
        damageCalc = (Global.playerStats["NormalDamage"] * Global.playerStatsMultiplier["NormalDamage"]/100) /2
        Global.playerStats["HP"] += damageCalc * Global.playerStats["LifeSteal"]/100
        text_label = TextLabel(
            text=f"-{round(damageCalc,1):g}HP",
            pos=target.pos,
            font_size=20,
            color=(225,0,0),
            font_name="Assets/Fonts/Minecraft.ttf",
            center=True,
        )
        text_label.moveTo(target.pos - pygame.Vector2(0,50), speed=300)
        text_label.fadeOut(speed=300, onDone=text_label.kill)
        Global.uiGroup.add(text_label)
        target.takeDamage(damageCalc)

        for _ in range(20):
            particlePos = target.pos[0] + random.randint(-20, 20), target.pos[1] + random.randint(-20, 20)
            Particle(
                groups=Global.mainAttackGroup, 
                pos=particlePos, 
                color=(232, 229, 61), 
                direction=pygame.Vector2(math.cos(random.uniform(0, 2 * math.pi)), 
                                            math.sin(random.uniform(0, 2 * math.pi))), 
                speed=random.randint(50, 150),
                size=random.randint(20, 60),
                fadeSpeed=500,
            )
    for i in range(6):
        Timer(i * 0.2, shoot, Global.timerGroup)