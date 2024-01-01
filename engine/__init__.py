################################################################################
### BOOTSTRAP                                                                ###
################################################################################

# XXX: Maybe there's another way to do this?
# XXX: I'd also like to put the window at the position it was in for the last
#      run, but it seems like this requires usage of some unrelated libraries
#      and might not be easy to make it cross platform. The basic idea I would
#      want to implement is to save the window position at shutdown, then
#      restore it at startup only if the window would be fully in the display.
#      Otherwise start at (0, 0).
import os
# For setting the window position when starting up. This needs to be done
# before pygame.display.set_mode().
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1528, 0)

# XXX: Pre-emptive initialization so it's ready for lib.text. Maybe do it early
#      in there instead?
import pygame
pygame.init()


################################################################################
### CONSTANTS                                                                ###
################################################################################

DISPLAY_WIDTH: int = 1024
DISPLAY_HEIGHT: int = 768
TICK_RATE: int = 30 # XXX: Hard coded to match model.battle.TICK_RATE
FRAME_RATE: int = TICK_RATE


################################################################################
### BASIC ENGINE COMPONENTS                                                  ###
################################################################################

from engine.grid import gridInit, gridCoordToScreen, gridRectToScreen, GRID_COLS, GRID_ROWS, GRID_STEP_X, GRID_STEP_Y
from engine.input import Input, InputEvent
from engine.input import (
    UP, DOWN, LEFT, RIGHT,
    CONFIRM, CANCEL, MENU, ACTION,
    START, SELECT,
)


################################################################################
### ENTITIES                                                                 ###
################################################################################
 
from engine.entity import Entity

from engine.battle import Battle
from engine.dialog import Dialog, DialogQuick
from engine.text import BasicText, PalletteText, PALLETTE_WHITE, PALLETTE_RED, PALLETTE_YELLOW


################################################################################
### ENGINE                                                                   ###
################################################################################
 
from engine.engine import add, remove, run
