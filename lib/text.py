import pygame

import lib.grid

GAME_FONT = pygame.font.SysFont('Courier New', 40, True)
FONT_ALIGN_HORIZONTAL = 3
FONT_ALIGN_VERTICAL = -3

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

def renderCharacter(ch: str):
    antialias = 1
    return GAME_FONT.render(ch, antialias, (0xFF, 0xFF, 0xFF))

class RenderText():
    def __init__(self, gsize: tuple[int, int], text: str):
        width, height = gsize
        self.gsize = gsize
        # self.tiles[y][x]
        self.tiles = [[None] * width for _ in range(height)]
        # "ch" for "character".
        for (chx, chy, ch) in streamPositionedCharacters(text):
            if chx < width and chy < height:
                self.tiles[chy][chx] = renderCharacter(ch)

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int]):
        width, height = self.gsize
        x, y = lib.grid.toScreen(gcoord)
        for chy in range(height):
            for chx in range(width):
                dx, dy = lib.grid.toScreen((chx, chy))
                tile = self.tiles[chy][chx]
                if tile is not None:
                    surface.blit(tile, (x + dx + FONT_ALIGN_HORIZONTAL, y + dy + FONT_ALIGN_VERTICAL))
