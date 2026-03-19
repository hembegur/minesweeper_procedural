import pygame, Global, random
from typing import Tuple
from Utils.Game.Highlight import highlight
from Utils.UiComponents.TextLabel import TextLabel

RGBA = Tuple[int, int, int, int]

class Tile(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: pygame.Vector2, index: pygame.Vector2, color: RGBA):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.clicked = False
        self.allyPlanted = None
        self.index = index
        self.isBomb = False
        self.revealed = False
        self.flagged = False
        self.pos = pos
        self.destroyed = False
        self.bombCount = 0

        self.textColor = (0, 0, 0)
        self.Text = TextLabel(
            text="",
            pos=pos,
            font_size=22,
            color=self.textColor, 
            font_name="Assets/Fonts/Pixel.TTF", 
            center=True,
            )
    def update(self):
        if self.revealed:
            Global.screen.blit(self.Text.image, self.Text.rect)
                

    def changeColor(self, color: RGBA):
        self.image.fill(color)

class createMap:
    def __init__(
            self, 
            cols: int, 
            rows: int, 
            offset: int, 
            color: RGBA,
            hiddenColor: RGBA,
            revealColor: RGBA,
            bombColor: RGBA,
            flagColor: RGBA,
            tileSize: pygame.Vector2 = pygame.Vector2(50, 50),
            mapPos: pygame.Vector2 = pygame.Vector2(0, 0),
            bombCount: int = 10,
        ):
        self.rows = rows
        self.cols = cols
        self.tileSize = tileSize
        self.mapPos = mapPos
        self.tilesGroup = pygame.sprite.Group()
        self.tilesArray = [[None for _ in range(cols)] for _ in range(rows)]
        self.tileGlow = True
        self.revealColor = revealColor
        self.bombColor = bombColor
        self.bombCount = bombCount
        self.flagColor = flagColor
        self.normalColor = color
        self.hiddenColor = hiddenColor
        self.firstClick = True

        # create map
        for row in range(rows):
            for col in range(cols):
                mapPosX, mapPosY = self.mapPos
                tileSizeX, tileSizeY = self.tileSize
                tile_x = mapPosX + col * (tileSizeX + offset)
                tile_y = mapPosY + row * (tileSizeY + offset)
                
                tile = Tile(
                    width=tileSizeX, 
                    height=tileSizeY,
                    pos=pygame.Vector2(tile_x, tile_y), 
                    index=pygame.Vector2(row, col),
                    color=color
                )
                self.tilesGroup.add(tile)
                self.tilesArray[row][col] = tile

    def mapDestroy(self, initialPos: pygame.Vector2, radius: int, shape: str):
        cx = int(initialPos.x)
        cy = int(initialPos.y)

        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                # bounds check
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    tile = self.tilesArray[x][y]
                    if shape == "square":
                        tile.kill()
                        tile.destroyed = True
                        #print("kill")
                    elif shape == "circle":
                        dx = x - cx
                        dy = y - cy
                        if dx*dx + dy*dy <= radius*radius:
                            tile.kill()
                            tile.destroyed = True
        self.calculateNumbers()

    def mapHidden(self, initialPos: pygame.Vector2, radius: int, shape: str):
        cx = int(initialPos.x)
        cy = int(initialPos.y)

        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                # bounds check
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    tile: Tile = self.tilesArray[x][y]
                    if shape == "square":
                        tile.revealed = False
                        tile.changeColor(self.hiddenColor)
                        #print("kill")
                    elif shape == "circle":
                        dx = x - cx
                        dy = y - cy
                        if dx*dx + dy*dy <= radius*radius:
                            tile.revealed = False
                            tile.changeColor(self.hiddenColor)
        self.calculateNumbers()

    def calculateNumbers(self):
        rows, cols = self.rows, self.cols
        # add numbers
        for row in range(rows):
            rows, cols = self.rows, self.cols
            for col in range(cols):
                currentTile: Tile = self.tilesArray[row][col]
                if currentTile.isBomb:
                    continue
                currentIndex = currentTile.index
                bombCount = 0
                x = int(currentIndex.x)
                y = int(currentIndex.y)
                for rowCheck in range(x-1,x+2):
                    for colCheck in range(y-1,y+2): 
                        if rowCheck < 0 or rowCheck > self.rows - 1 or colCheck < 0 or colCheck > self.cols - 1:
                            continue
                        checkTile: Tile = self.tilesArray[rowCheck][colCheck]
                        bombCount += 1 if checkTile.isBomb and not checkTile.destroyed else 0
                    
                currentTile.Text.setText(str(bombCount))
                currentTile.bombCount = bombCount
    
    def generateBomb(self, initialTile: Tile):
        rows, cols = self.rows, self.cols
        # place som bom
        for _ in range(self.bombCount):
            selectedTile : Tile = self.tilesArray[random.randint(0, rows-1)][random.randint(0, cols-1)] 
            while selectedTile.isBomb or selectedTile == initialTile:
                selectedTile : Tile = self.tilesArray[random.randint(0, rows-1)][random.randint(0, cols-1)] 
            selectedTile.isBomb = True
            selectedTile.Text.setText("B")
        self.calculateNumbers()

    #### wat reveal and bom does
    def successfulReveal(self):
        Global.playerMP += 1 if Global.playerMP < Global.playerMaxMP else 0
    
    def bombReveal(self):
        Global.playerHP -= 10

    def tileReveal(self, currentTile: Tile, first: bool):
        if (currentTile.isBomb) and first and not currentTile.flagged:
            currentTile.revealed = True
            currentTile.changeColor(self.bombColor)
            self.bombReveal()
            return
        elif currentTile.isBomb or currentTile.revealed or currentTile.flagged or currentTile.destroyed:
            return
        
        currentTile.changeColor(self.revealColor)
        currentTile.revealed = True
        if first:
            self.successfulReveal()

        if currentTile.bombCount > 0:
            return
        currentIndex = currentTile.index
        x = int(currentIndex.x)
        y = int(currentIndex.y)

        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if (dx or dy) and 0 <= x+dx < self.rows and 0 <= y+dy < self.cols:
                    self.tileReveal(self.tilesArray[x+dx][y+dy], False)

    def quickTileReveal(self, currentTile: Tile):
        if not currentTile.revealed:
            return
        flagCount = 0
        currentIndex = currentTile.index
        x = int(currentIndex.x)
        y = int(currentIndex.y)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if (dx or dy) and 0 <= x+dx < self.rows and 0 <= y+dy < self.cols:
                    chosenTile: Tile = self.tilesArray[x+dx][y+dy]
                    if chosenTile.flagged or (chosenTile.isBomb and chosenTile.revealed):
                        flagCount += 1
        if flagCount >= currentTile.bombCount:
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    chosenTile: Tile = self.tilesArray[x+dx][y+dy]
                    if (dx or dy) and 0 <= x+dx < self.rows and 0 <= y+dy < self.cols and not chosenTile.revealed:
                        self.tileReveal(chosenTile, True)
                    
    def handleClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for tile in self.tilesGroup:
                if tile.rect.collidepoint(mouse_pos) and not tile.flagged:
                    if self.firstClick:
                        self.firstClick = False
                        self.generateBomb(tile)
                    if tile.revealed:
                        self.quickTileReveal(tile)
                    self.tileReveal(tile, True)
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = event.pos
            for tile in self.tilesGroup:
                if tile.rect.collidepoint(mouse_pos):
                    if not tile.revealed:
                        tile.flagged = not tile.flagged
                        if tile.flagged:
                            tile.changeColor(self.flagColor)
                        else:
                            tile.changeColor(self.normalColor)
                        break
                        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for tile in self.tilesGroup:
                if tile.clicked:
                    tile.clicked = False
                    break 

    def update(self):            
        self.tilesGroup.draw(Global.screen)
        self.tilesGroup.update()

        for tile in self.tilesGroup:
            mousePos = pygame.mouse.get_pos()
            # hover glow
            if tile.rect.collidepoint(mousePos) and self.tileGlow:
                highlight(tile.rect.size, tile.rect.topleft, (150, 150, 150, 60))

            if tile.clicked:
                highlight(tile.rect.size, tile.rect.topleft, (150, 150, 150, 80))