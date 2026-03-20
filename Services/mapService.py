import pygame
import Global
import random
from typing import Tuple
from Utils.Game.Highlight import highlight
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
    }


# ──────────────────────────────────────────────
# Map operations
# ──────────────────────────────────────────────

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
                if shape == "square":
                    tile["destroyed"] = True
                    m["tilesArray"][x][y] = None          # "kill" the tile
                elif shape == "circle":
                    dx, dy = x - cx, y - cy
                    if dx*dx + dy*dy <= radius*radius:
                        tile["destroyed"] = True
                        m["tilesArray"][x][y] = None

    calculate_numbers(m)


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

def on_successful_reveal():
    if Global.playerMP < Global.playerMaxMP:
        Global.playerMP += 1


def on_bomb_reveal():
    Global.playerHP -= 10


def tile_reveal(m: dict, tile: dict, first: bool):
    if tile["isBomb"] and first and not tile["flagged"] and not tile["revealed"]:
        tile["revealed"] = True
        tile_change_color(tile, m["bombColor"])
        on_bomb_reveal()
        return

    if tile["isBomb"] or tile["revealed"] or tile["flagged"] or tile["destroyed"]:
        return

    tile_change_color(tile, m["revealColor"])
    tile["revealed"] = True

    if first:
        on_successful_reveal()

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
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                tile["flagged"] = not tile["flagged"]
                color = m["flagColor"] if tile["flagged"] else m["normalColor"]
                tile_change_color(tile, color)
                break

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        for tile in map_all_tiles(m):
            if tile["clicked"]:
                tile["clicked"] = False
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