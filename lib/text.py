import pygame

from functools import cache

import lib.grid

GAME_FONT = pygame.font.SysFont('Courier New', 40, True) # XXX: Bundle a basic font, perhaps.
FONT_ALIGN_HORIZONTAL = 4
FONT_ALIGN_VERTICAL = -3

# These must be 0, 1, and 2 respectively!
PALLETTE_WHITE = 0
PALLETTE_RED = 1
PALLETTE_YELLOW = 2

def streamPositionedCharacters(text: str):
    # XXX: This could have a pre-processed text wrapping integrated with it? Or just having one available would be helpful?
    x, y = 0, 0
    for c in text:
        if c == '\n':
            x = 0
            y += 1
        else:
            yield x, y, c
            x += 1

@cache
def renderCharacter(ch: str, color: pygame.Color = (0xFF, 0xFF, 0xFF)):
    antialias = 1
    return GAME_FONT.render(ch, antialias, color)

class BasicText():
    def __init__(self, gsize: tuple[int, int], text: str, color: pygame.Color = (0xFF, 0xFF, 0xFF)):
        width, height = gsize
        self.gsize = gsize
        # self.tiles[y][x]
        self.tiles = [[None] * width for _ in range(height)]
        # "ch" for "character".
        for (chx, chy, ch) in streamPositionedCharacters(text):
            if chx < width and chy < height:
                self.tiles[chy][chx] = renderCharacter(ch, color = color)

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int]):
        width, height = self.gsize
        x, y = lib.grid.toScreen(gcoord)
        for chy in range(height):
            for chx in range(width):
                dx, dy = lib.grid.toScreen((chx, chy))
                tile = self.tiles[chy][chx]
                if tile is not None:
                    surface.blit(tile, (x + dx + FONT_ALIGN_HORIZONTAL, y + dy + FONT_ALIGN_VERTICAL))
RenderText = BasicText # TODO: Do a project-wide rename to BasicText.

class PalletteText():
    def __init__(self, gsize: tuple[int, int], text: str):
        self.texts: list[BasicText] = [
            BasicText(gsize, text, color = (0xFF, 0xFF, 0xFF)), # PALLETTE_WHITE
            BasicText(gsize, text, color = (0xFF, 0x11, 0x11)), # PALLETTE_RED
            BasicText(gsize, text, color = (0xFF, 0xFF, 0x22)), # PALLETTE_YELLOW
        ]

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int], pallette = PALLETTE_WHITE):
        self.texts[pallette].render(surface, gcoord)

def pad(text: str, length: int):
    if len(text) < length:
        return ' ' * (length - len(text)) + text
    return text

DIGITS = [PalletteText((1, 1), str(i)) for i in range(10)]

def renderDigits(surface: pygame.Surface, grect: tuple[int, int, int, int], text: str, pallette = PALLETTE_WHITE):
    x, y, width, _ = grect
    for i in range(width):
        if i < len(text):
            o = ord(text[i]) - ord('0')
            if o >= 0 and o <= 9:
                DIGITS[o].render(surface, (x, y), pallette = pallette)
        x += 1
