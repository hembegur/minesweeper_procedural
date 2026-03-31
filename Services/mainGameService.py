import pygame, Global, random
from Utils.UiComponents.TextLabel import TextLabel
from Utils.UiComponents.Box import Box
from Utils.Game.mathStuff import Timer
from Services.mapService import create_map, handle_click, map_update, mapLock, mapUnLock

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        size: pygame.Vector2,
        groups=None,
        imagePath: str = None,
        color: tuple = (255, 255, 255, 255),
        layer: int = 0,
    ):
        super().__init__()
        if groups is not None:
            if isinstance(groups, (list, tuple)):
                for g in groups:
                    g.add(self, layer=layer)
            else:
                groups.add(self, layer=layer)

        self.pos  = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.image = Global.loadImage(imagePath, (int(size.x), int(size.y)))
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, direction: pygame.Vector2, speed: float, dt: float = None):
        dt = dt or Global.mainBackGroundDt
        if direction.length() == 0:
            return
        self.pos += direction.normalize() * speed * dt
        self.rect.center = self.pos

    def moveTo(self, destination: pygame.Vector2, speed: float, dt: float = None):
        dt    = dt or Global.mainBackGroundDt
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
        self.move(pygame.Vector2(-1, 0), speed=200, dt=Global.mainBackGroundDt)
        if (
            self.pos[0] < -200 or
            self.pos[0] > Global.mainGameBox.size.x + 200 or
            self.pos[1] < -200 or
            self.pos[1] > Global.mainGameBox.size.y + 200
        ):
            self.kill()
       # Global.mainGameBox.canvas.blit(self.image, self.rect)

from Classes.Enemies.SpikeEnemy import SpikeEnemy
from Classes.Enemies.LaserEnemy import LaserEnemy
from Classes.Enemies.ClownEnemy import ClownEnemy
from Classes.Enemies.MinigunEnemy import MinigunEnemy
ENEMY_REGISTRY = {
    "SpikeEnemy": SpikeEnemy,
    "LaserEnemy": LaserEnemy,
    "ClownEnemy": ClownEnemy,
    "MinigunEnemy": MinigunEnemy,
}

class mainGameService:
    def __init__(self):
        self.bgSpawnCD = (0.5,1)
        self.bgCurrentSpawn = 0 
        Global.mainBackGroundDt = Global.dt
        self.shopSprite = None
        self.shop = None
        #groundBox
        currSize = pygame.Vector2(750,700)
        ground = Box(
            pos=pygame.Vector2(0,175),
            size=currSize,
            groups=Global.mainBackGroundGroup,
            color=(245, 245, 245, 255),
            border=True,
            borderColor=(100, 100, 100, 255),
            borderWidth=5,
            borderRadius=0,
        )
        Global.mainBackGroundGroup.add(ground)
        self.create_and_position_map()

    def create_and_position_map(self):
        mapSize = (random.randint(5,15), random.randint(5,15))
        tileSize = (50,50)
        offset = 2
        boxRect = Global.minesweeperBox.rect
        mapPos = (
            boxRect.x + (boxRect.width- (mapSize[0] * (tileSize[0] + offset) - offset)) / 2  + tileSize[0] / 2,
            boxRect.y + (boxRect.height - (mapSize[1] * (tileSize[1] + offset) - offset)) / 2  + tileSize[1] / 2,
        )
        Global.currentMap = create_map(
            cols=mapSize[0],
            rows=mapSize[1],
            offset=offset,
            color=(100,100,100,255),
            hiddenColor=(50,50,50,255),
            revealColor=(200,200,200,255),
            bombColor=(255,50,50,255),
            flagColor=(220,220,0),
            mapPos=mapPos,
            tileSize=tileSize,
            bombCount=int((mapSize[0] * mapSize[1]) * 0.1)
        )

    def stop(self,stop: bool):
        if stop:
            self.dt = 0
    
    def update(self):
        if Global.gameState == "Playing":
            Global.mainBackGroundDt = Global.dt

        self.bgCurrentSpawn -= Global.mainBackGroundDt
        if self.bgCurrentSpawn <= 0: 
            randomSize = random.randint(150,250)
            SimpleSprite(
                pos=pygame.Vector2(900, 100 - (randomSize/2 - 100)),
                size=pygame.Vector2(randomSize,randomSize),
                groups=Global.mainBackGroundGroup,
                imagePath=random.choice(["Assets/Background/house1.png", "Assets/Background/tree.png"]),
            )
            self.bgCurrentSpawn = random.uniform(self.bgSpawnCD[0], self.bgSpawnCD[1])
        
        map_update(Global.currentMap)

        #|----------------------------Game Loop

        if Global.gameState == "Preparing":
            gameProgress = Global.gameProgress[Global.currentDifficulty]
            self.enemySpawnCD = gameProgress["SpawnRate"]
            self.enemyLastSpawn = 2
            self.currentEnemies = gameProgress[f"Round{Global.currentRound}"].copy()
            Global.gameState = "Playing"
            self.shopSprite = None

        if Global.gameState == "Playing":
            self.enemyLastSpawn -= Global.mainBackGroundDt

            # Enemy left check
            enemyLeft = [k for k, v in self.currentEnemies.items() if v.get("InGame", 0) > 0 or v["EnemyLeft"] > 0] 

            if not enemyLeft:
                Global.gameState = "Shop"

            # spawn Enemies
            if self.enemyLastSpawn <= 0:
                self.enemyLastSpawn = random.uniform(self.enemySpawnCD[0], self.enemySpawnCD[1])

                available = [k for k, v in self.currentEnemies.items() 
                 if v.get("InGame", 0) < v["MaxEnemy"] and v["EnemyLeft"] > 0]

                if not available:
                    return  # all at max, skip this spawn tick

                chosenEnemy = random.choice(available)
                enemyData   = self.currentEnemies[chosenEnemy]

                if "InGame" not in enemyData:
                    enemyData["InGame"] = 0

                newEnemy = ENEMY_REGISTRY[chosenEnemy](
                    pos=pygame.Vector2(random.randint(450, 650), random.randint(100, 450)),
                    size=pygame.Vector2(200, 200),
                    groups=Global.entityGroup,
                )
                Global.entityGroup.add(newEnemy)

                enemyData["InGame"]   += 1
                enemyData["EnemyLeft"] -= 1

                def removal():
                    enemyData["InGame"] -= 1
                newEnemy.dieFunction = removal

            if Global.currentMap["completed"]:
                self.create_and_position_map()

        if Global.gameState == "Shop":
            #Global.currentRound += 1
            if not self.shopSprite:
                self.shopSprite = SimpleSprite(
                    pos=pygame.Vector2(900, 150),
                    size=pygame.Vector2(200,200),
                    groups=Global.mainBackGroundGroup,
                    imagePath="Assets/Background/shop.png",
                    layer=999,
                )
            
            if self.shopSprite.pos.x <= 400:
                Global.mainBackGroundDt = 0
                Global.gameState = "Buying"
                self.shop = None
            else:
                Global.mainBackGroundDt = Global.dt
        if Global.gameState == "Buying":
            if not self.shop:
                for sprite in list(Global.msAttackGroup):
                    sprite.kill()
                Global.msParticleGroup.empty()
                mapLock(Global.currentMap)
                self.shop = Global.UiService.spawnShop()

            if self.shop.removed:
                mapUnLock(Global.currentMap)
                Global.currentRound += 1
                Global.gameState = "Preparing"