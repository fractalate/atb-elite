import pygame

from functools import cache

import engine.grid

GAME_FONT = pygame.font.SysFont('Courier New', 40, True) # XXX: Bundle a basic font, perhaps.
FONT_ALIGN_HORIZONTAL = 4
FONT_ALIGN_VERTICAL = -5 # XXX: -3 looked good, but low chars like y hang over the dialog border

class Pallette(int): pass

# These must be 0, 1, and 2 respectively!
PALLETTE_WHITE: Pallette = 0
PALLETTE_RED: Pallette = 1
PALLETTE_YELLOW: Pallette = 2

_PALLETTES = [PALLETTE_WHITE, PALLETTE_RED, PALLETTE_YELLOW]

_WHITE = pygame.Color(0xFF, 0xFF, 0xFF)
_RED = pygame.Color(0xFF, 0x11, 0x11)
_YELLOW = pygame.Color(0xFF, 0xFF, 0x22)

_COLORS = [_WHITE, _RED, _YELLOW]

def _streamPositionedCharacters(text: str):
    x, y = 0, 0
    for c in text:
        if c == '\n':
            x = 0
            y += 1
        else:
            yield x, y, c
            x += 1

@cache
def _renderCharacter(ch: str, pallette: Pallette):
    antialias = 1
    return GAME_FONT.render(ch, antialias, _COLORS[pallette])

class BasicText():
    def __init__(self, gsize: tuple[int, int], text: str, pallette: Pallette = PALLETTE_WHITE):
        width, height = gsize
        self.gsize: tuple[int, int] = gsize
        # self.tiles[y][x]
        self.tiles: list[list[None | pygame.Surface]] = [[None] * width for _ in range(height)]
        # "ch" for "character".
        for (chx, chy, ch) in _streamPositionedCharacters(text):
            if chx < width and chy < height:
                self.tiles[chy][chx] = _renderCharacter(ch, pallette)

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int]):
        width, height = self.gsize
        x, y = engine.gridCoordToScreen(gcoord)
        for chy in range(height):
            for chx in range(width):
                dx, dy = engine.grid.gridCoordToScreen((chx, chy))
                tile = self.tiles[chy][chx]
                if tile is not None:
                    surface.blit(tile, (x + dx + FONT_ALIGN_HORIZONTAL, y + dy + FONT_ALIGN_VERTICAL))

class PalletteText():
    def __init__(self, gsize: tuple[int, int], text: str):
        self.texts: list[BasicText] = [BasicText(gsize, text, pallette) for pallette in _PALLETTES]

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int], pallette = PALLETTE_WHITE):
        self.texts[pallette].render(surface, gcoord)
