'''
This module defines "the grid" on which certain aspects of the game operate.
Chiefly, this is used for the positioning of text and dialogs.

IMPORTANT:

Always call lib.grid.init() in case resolutions are dynamic at some later stage
of development.
'''

import pygame

import lib.sys

GRID_COLS = 32
GRID_ROWS = 24
GRID_STEP_X = lib.sys.DISPLAY_WIDTH // GRID_COLS # Don't forget to call init().
GRID_STEP_Y = lib.sys.DISPLAY_HEIGHT // GRID_ROWS # Don't forget call init().

def init(surface: pygame.Surface):
    global GRID_STEP_X
    global GRID_STEP_Y
    width, height = surface.get_size()
    GRID_STEP_X = width // GRID_COLS
    GRID_STEP_Y = height // GRID_ROWS

def toScreen(coordinate: tuple[int, int]):
    return (coordinate[0] * GRID_STEP_X, coordinate[1] * GRID_STEP_Y)

# Useful for debugging.
def draw(surface: pygame.Surface):
    width, height = surface.get_size()
    for y in range(GRID_ROWS):
        pygame.draw.line(surface, 0xFFFFFF, (0, y * GRID_STEP_Y), (width, y * GRID_STEP_Y))
    for x in range(GRID_COLS):
        pygame.draw.line(surface, 0xFFFFFF, (x * GRID_STEP_X, 0), (x * GRID_STEP_X, height))
