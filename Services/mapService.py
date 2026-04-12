import pygame
import Global
import random
from typing import Tuple
from Utils.Game.Highlight import highlight
from Utils.Game.mathStuff import Timer
from Utils.UiComponents.TextLabel import TextLabel

RGBA = Tuple[int, int, int, int]

# ──────────────────────────────────────────────
# Tile data  (plain dict, no class)
# ──────────────────────────────────────────────

def create_tile(width: int, height: int, pos: pygame.Vector2,
                index: pygame.Vector2, color: RGBA, textColor: RGBA = (0, 0, 0)) -> dict:
    image = pygame.Surface([width, height], pygame.SRCALPHA)
    image.fill(color)
    rect = image.get_rect()
    rect.center = (int(pos.x), int(pos.y))

    text_label = TextLabel(
        text="",
        pos=pos,
        font_size=30,
        color=textColor,
        font_name="Assets/Fonts/Pixel.TTF",
        center=True,
    )

    return {
        "image":       image,
        "rect":        rect,
        "clicked":     False,
        "allyPlanted": None,
        "index":       index,
        "isBomb":      False,
        "revealed":    False,
        "flagged":     False,
        "pos":         pos,
        "destroyed":   False,
        "bombCount":   0,
        "Text":        text_label,
    }


def tile_change_color(tile: dict, color: RGBA):
    tile["image"].fill(color)

def tile_update(tile: dict):
    if tile["revealed"]:
        Global.screen.blit(tile["Text"].image, tile["Text"].rect)


# ──────────────────────────────────────────────
# Map data  (plain dict, no class)
# ──────────────────────────────────────────────

def create_map(
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
) -> dict:

    #tiles_group = pygame.sprite.Group()   # kept for draw() convenience
    tiles_array = [[None for _ in range(cols)] for _ in range(rows)]

    tileSizeX, tileSizeY = tileSize
    mapPosX,   mapPosY   = mapPos

    for row in range(rows):
        for col in range(cols):
            tile_x = mapPosX + col * (tileSizeX + offset)
            tile_y = mapPosY + row * (tileSizeY + offset)

            tile = create_tile(
                width=tileSizeX,
                height=tileSizeY,
                pos=pygame.Vector2(tile_x, tile_y),
                index=pygame.Vector2(row, col),
                color=color,
            )
            tiles_array[row][col] = tile

    return {
        "rows":        rows,
        "cols":        cols,
        "tileSize":    tileSize,
        "mapPos":      mapPos,
        "tilesArray":  tiles_array,
        "tileGlow":    True,
        "revealColor": revealColor,
        "bombColor":   bombColor,
        "bombCount":   bombCount,
        "flagColor":   flagColor,
        "normalColor": color,
        "hiddenColor": hiddenColor,
        "firstClick":  True,
        "mapLock":  False,
        "remaining": (rows * cols) - bombCount,
        "completed": False,
    }


# ──────────────────────────────────────────────
# Map operations
# ──────────────────────────────────────────────

def mapLock(m: dict):
    m["savedRevealState"] = {}
    m["mapLock"] = True
    for tile in map_all_tiles(m):
        m["savedRevealState"][id(tile)] = tile["revealed"]
        tile["revealed"] = False
        tile_change_color(tile, m["hiddenColor"])

def mapUnLock(m: dict):
    if "savedRevealState" not in m:
        return
    m["mapLock"] = False
    for tile in map_all_tiles(m):
        wasRevealed = m["savedRevealState"].get(id(tile), False)
        tile["revealed"] = wasRevealed
        if wasRevealed:
            tile_change_color(tile, m["revealColor"])
            if tile["isBomb"]:
                tile_change_color(tile, m["bombColor"])
        else:
            tile_change_color(tile, m["normalColor"])
            if tile["flagged"]:
                tile_change_color(tile, m["flagColor"])

def map_all_tiles(m: dict):
    """Flat iterator over every tile (skips None slots)."""
    for row in m["tilesArray"]:
        for tile in row:
            if tile is not None:
                yield tile


def map_destroy(m: dict, initialPos: pygame.Vector2, radius: int, shape: str):
    cx, cy = int(initialPos.x), int(initialPos.y)

    for x in range(cx - radius, cx + radius + 1):
        for y in range(cy - radius, cy + radius + 1):
            if 0 <= x < m["rows"] and 0 <= y < m["cols"]:
                tile = m["tilesArray"][x][y]
                if tile is None:
                    continue
                if shape == "square":
                    _destroyTile(m, tile, x, y)
                elif shape == "circle":
                    dx, dy = x - cx, y - cy
                    if dx*dx + dy*dy <= radius*radius:
                        _destroyTile(m, tile, x, y)

    calculate_numbers(m)


def _destroyTile(m: dict, tile: dict, x: int, y: int):
    # adjust remaining count — only count tiles that haven't been revealed and aren't bombs
    if not tile["revealed"] and not tile["isBomb"]:
        m["remaining"] -= 1
    tile["destroyed"] = True
    m["tilesArray"][x][y] = None


def map_hidden(m: dict, initialPos: pygame.Vector2, radius: int, shape: str):
    cx, cy = int(initialPos.x), int(initialPos.y)

    for x in range(cx - radius, cx + radius + 1):
        for y in range(cy - radius, cy + radius + 1):
            if 0 <= x < m["rows"] and 0 <= y < m["cols"]:
                tile = m["tilesArray"][x][y]
                if tile is None:
                    continue
                if shape == "square":
                    tile["revealed"] = False
                    tile_change_color(tile, m["hiddenColor"])
                elif shape == "circle":
                    dx, dy = x - cx, y - cy
                    if dx*dx + dy*dy <= radius*radius:
                        tile["revealed"] = False
                        tile_change_color(tile, m["hiddenColor"])

    calculate_numbers(m)

number_colors = {
    0: (0, 0, 0),
    1: (0, 0, 255),       # Blue
    2: (0, 128, 0),       # Green
    3: (255, 0, 0),       # Red
    4: (0, 0, 128),       # Dark Blue
    5: (128, 0, 0),       # Dark Red / Maroon
    6: (0, 128, 128),     # Teal / Cyan
    7: (0, 0, 0),         # Black
    8: (128, 128, 128),   # Gray
}

def calculate_numbers(m: dict):
    rows, cols = m["rows"], m["cols"]
    for row in range(rows):
        for col in range(cols):
            tile = m["tilesArray"][row][col]
            if tile is None or tile["isBomb"]:
                continue
            x, y = int(tile["index"].x), int(tile["index"].y)
            bomb_count = 0
            for rx in range(x - 1, x + 2):
                for ry in range(y - 1, y + 2):
                    if 0 <= rx < rows and 0 <= ry < cols:
                        neighbour = m["tilesArray"][rx][ry]
                        if neighbour and neighbour["isBomb"] and not neighbour["destroyed"]:
                            bomb_count += 1
            if bomb_count > 0:
                tile["Text"].setText(str(bomb_count))
                tile["Text"].setColor(number_colors[bomb_count])
            else:
                tile["Text"].setText("")
            tile["bombCount"] = bomb_count


def generate_bombs(m: dict, initial_tile: dict):
    rows, cols = m["rows"], m["cols"]
    placed = 0
    while placed < m["bombCount"]:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        candidate = m["tilesArray"][r][c]
        if candidate and not candidate["isBomb"] and candidate is not initial_tile:
            candidate["isBomb"] = True
            candidate["Text"].setText("B")
            placed += 1
    calculate_numbers(m)


# ──────────────────────────────────────────────
# Reveal logic
# ──────────────────────────────────────────────

def on_successful_reveal(tile: dict, m : map):
    sfx = random.choice([
        "Assets/Sounds/SoundEffect/tile_reveal1.wav",
        "Assets/Sounds/SoundEffect/tile_reveal2.wav"
    ])
    Global.SoundManager.playSFX(sfx, 0.5)
    if Global.playerStats["MP"] < Global.playerStats["MaxMP"]:
        text_label = TextLabel(
            text="+1MP",
            pos=tile["pos"],
            font_size=20,
            color=(50,50,255),
            font_name="Assets/Fonts/Minecraft.ttf",
            center=True,
        )
        text_label.moveTo(tile["pos"] - pygame.Vector2(0,50), speed=300)
        text_label.fadeOut(speed=300, onDone=text_label.kill)
        Global.uiGroup.add(text_label)

        Global.playerStats["MP"] += Global.playerStatsGain["MP"]
        if Global.playerStats["MP"] > Global.playerStats["MaxMP"]:
            Global.playerStats["MP"] = Global.playerStats["MaxMP"]


def on_bomb_reveal(tile: dict):
    sfx = random.choice([
        "Assets/Sounds/SoundEffect/explosion_small.wav",
        "Assets/Sounds/SoundEffect/explosion_quick.wav"
    ])
    Global.SoundManager.playSFX(sfx, 1.5)
    text_label = TextLabel(
        text="-10HP",
        pos=tile["pos"],
        font_size=20,
        color=(225,0,0),
        font_name="Assets/Fonts/Minecraft.ttf",
        center=True,
    )
    text_label.moveTo(tile["pos"] - pygame.Vector2(0,50), speed=300)
    text_label.fadeOut(speed=300, onDone=text_label.kill)
    Global.uiGroup.add(text_label)

    Global.playerStats["HP"] -= int(30 * (1 + Global.difficultyScale[Global.currentDifficulty]["DamageScale"] * Global.currentRound))


def tile_reveal(m: dict, tile: dict, first: bool):
    if tile["isBomb"] and first and not tile["flagged"] and not tile["revealed"]:
        tile["revealed"] = True
        tile_change_color(tile, m["bombColor"])
        on_bomb_reveal(tile)
        return

    if tile["isBomb"] or tile["revealed"] or tile["flagged"] or tile["destroyed"]:
        return

    tile_change_color(tile, m["revealColor"])
    tile["revealed"] = True
    m["remaining"] -= 1

    if first:
        on_successful_reveal(tile, m)

    if tile["bombCount"] > 0:
        return

    x, y = int(tile["index"].x), int(tile["index"].y)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx or dy) and 0 <= x + dx < m["rows"] and 0 <= y + dy < m["cols"]:
                neighbour = m["tilesArray"][x + dx][y + dy]
                if neighbour:
                    tile_reveal(m, neighbour, False)


def quick_tile_reveal(m: dict, tile: dict):
    if not tile["revealed"] or tile["isBomb"]:
        return
    x, y = int(tile["index"].x), int(tile["index"].y)
    flag_count = 0

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx or dy) and 0 <= x + dx < m["rows"] and 0 <= y + dy < m["cols"]:
                neighbour = m["tilesArray"][x + dx][y + dy]
                if neighbour and (neighbour["flagged"] or
                                  (neighbour["isBomb"] and neighbour["revealed"])):
                    flag_count += 1

    if flag_count >= tile["bombCount"]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx or dy) and 0 <= x + dx < m["rows"] and 0 <= y + dy < m["cols"]:
                    neighbour = m["tilesArray"][x + dx][y + dy]
                    if neighbour and not neighbour["revealed"]:
                        tile_reveal(m, neighbour, True)


# ──────────────────────────────────────────────
# Input
# ──────────────────────────────────────────────

def handle_click(m: dict, event: pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        for tile in map_all_tiles(m):
            if tile["clicked"]:
                tile["clicked"] = False
                break

    if m["mapLock"]:
        return
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not Global.MainGameService.mapHidden:
        mouse_pos = event.pos
        for tile in map_all_tiles(m):
            if tile["rect"].collidepoint(mouse_pos) and not tile["flagged"]:
                if m["firstClick"]:
                    m["firstClick"] = False
                    generate_bombs(m, tile)
                if tile["revealed"]:
                    quick_tile_reveal(m, tile)
                tile_reveal(m, tile, True)
                break

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        mouse_pos = event.pos
        for tile in map_all_tiles(m):
            if tile["rect"].collidepoint(mouse_pos) and not tile["revealed"]:
                sfx = random.choice([
                    "Assets/Sounds/SoundEffect/flag.wav",
                    "Assets/Sounds/SoundEffect/flag2.wav",
                    "Assets/Sounds/SoundEffect/flag3.wav",
                ])
                Global.SoundManager.playSFX(sfx, 0.2)
                tile["flagged"] = not tile["flagged"]
                color = m["flagColor"] if tile["flagged"] else m["normalColor"]
                tile_change_color(tile, color)
                break


# ──────────────────────────────────────────────
# Draw / update  (called every frame)
# ──────────────────────────────────────────────

def map_update(m: dict):
    mouse_pos = pygame.mouse.get_pos()

    for tile in map_all_tiles(m):
        # draw tile surface
        Global.screen.blit(tile["image"], tile["rect"])

        # draw number / bomb label
        tile_update(tile)

        # hover glow
        if tile["rect"].collidepoint(mouse_pos) and m["tileGlow"]:
            highlight(tile["rect"].size, tile["rect"].topleft, (150, 150, 150, 60))

        # click glow
        if tile["clicked"]:
            highlight(tile["rect"].size, tile["rect"].topleft, (150, 150, 150, 80))

        #print(m["remaining"])
        if m["remaining"] <= 0 and not m["completed"]:
            # make sure there are actually no unrevealed non-bomb tiles left
            unrevealed = sum(
                1 for tile in map_all_tiles(m)
                if not tile["revealed"] and not tile["isBomb"]
            )
            if unrevealed <= 0:
                m["completed"] = True
                if Global.playerStats["Ult"] < Global.playerStats["MaxUlt"]:
                    Global.playerStats["Ult"] += 1

                    middle = pygame.Vector2(Global.screenWidth/2, Global.screenHeight/2)
                    text_label = TextLabel(
                        text="+1ULT",
                        pos=middle,
                        font_size=100,
                        color=(200,0,200),
                        font_name="Assets/Fonts/Minecraft.ttf",
                        center=True,
                    )
                    text_label.moveTo(middle + pygame.Vector2(0,-100), speed=300 )
                    text_label.fadeOut(speed=300, onDone=text_label.kill)
                    Global.uiGroup.add(text_label)