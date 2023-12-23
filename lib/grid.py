'''
This module defines "the grid" on which certain aspects of the game operate.
Chiefly, this is used for the positioning of text and dialogs.

IMPORTANT:

Some sane defaults are set for GRID_STEP_X and GRID_STEP_Y, but if the
resolution of the game is ever not 1024x768, then the values will be wrong.
Always call lib.grid.init().
'''

import pygame

GRID_COLS = 32
GRID_ROWS = 24
GRID_STEP_X = 1024 // GRID_COLS # Don't forget to call init().
GRID_STEP_Y = 768 // GRID_ROWS # Don't forget call init().

def init(surface: pygame.Surface):
    global GRID_STEP_X
    global GRID_STEP_Y
    width, height = surface.get_size()
    GRID_STEP_X = width // GRID_COLS
    GRID_STEP_Y = height // GRID_ROWS

def toScreen(coordinate: tuple[int, int]):
    return (coordinate[0] * GRID_STEP_X, coordinate[1] * GRID_STEP_Y)

def draw(surface: pygame.Surface):
    width, height = surface.get_size()
    for y in range(GRID_ROWS):
        pygame.draw.line(surface, 0xFFFFFF, (0, y * GRID_STEP_Y), (width, y * GRID_STEP_Y))
    for x in range(GRID_COLS):
        pygame.draw.line(surface, 0xFFFFFF, (x * GRID_STEP_X, 0), (x * GRID_STEP_X, height))
