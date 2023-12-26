import pygame

import lib.dialog
import lib.fighter
import lib.grid

# XXX: Is there a better way to name simple types for type hinting?
SideNo = int
ZoneNo = str # ZONE_LEFT, ZONE_RIGHT, ZONE_MID

# Player's side is side 0.
# All other fighters' sides are 1 or greater. Typically, it's 1.
SIDE_PLAYER = 0

ZONE_LEFT = 'left'
ZONE_RIGHT = 'right'
ZONE_MID = 'mid'

ZONE_COLS = 3
ZONE_ROWS = 4 # This value is not really changeable. Use 4 to match the party size.

HALF = lib.grid.toScreen((1, 1))
HALF = (HALF[0] // 2, HALF[1] // 2)

# Piggy backing on the grid system to lay out the battle zones' land.
LAND_X, LAND_Y = lib.grid.toScreen((0, 10))
LAND_WIDTH, LAND_HEIGHT = lib.grid.toScreen((32, 10))
LAND_LEFT_TOP_X, LAND_LEFT_TOP_Y = lib.grid.toScreen((3, 10))
LAND_LEFT_BOTTOM_X, LAND_LEFT_BOTTOM_Y = lib.grid.toScreen((0, 20))
LAND_RIGHT_TOP_X, LAND_RIGHT_TOP_Y = lib.grid.toScreen((23, 10))
LAND_RIGHT_BOTTOM_X, LAND_RIGHT_BOTTOM_Y = lib.grid.toScreen((26, 20))
LAND_MID_TOP_X, LAND_MID_TOP_Y = lib.grid.toScreen((13, 10))
LAND_MID_BOTTOM_X, LAND_MID_BOTTOM_Y = lib.grid.toScreen((13, 20))
def addHalfY(coord):
    x, y = coord
    return (x, y + HALF[1])
LAND_COL_WIDTH, LAND_COL_HEIGHT = addHalfY(lib.grid.toScreen((2, 2))) # (2, 2.5)

def getCenter(zone, coord: tuple[int, int]):
    if zone == ZONE_LEFT:
        col, row = coord
        x_shift = (LAND_LEFT_TOP_X - LAND_LEFT_BOTTOM_X) * (ZONE_ROWS - row - 1) // ZONE_ROWS + HALF[0]
        return (
            LAND_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 + x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == ZONE_RIGHT:
        col, row = coord
        x_shift = (LAND_RIGHT_TOP_X - LAND_RIGHT_BOTTOM_X) * (row) // ZONE_ROWS - HALF[0]
        return (
            LAND_RIGHT_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 - x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == ZONE_MID:
        col, row = coord
        return (
            LAND_MID_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    return lib.grid.toScreen(coord)

def drawZones(surface: pygame.Surface):
    for i in range(ZONE_ROWS):
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_X, LAND_Y + LAND_COL_HEIGHT * i),
                        (LAND_X + LAND_WIDTH, LAND_Y + LAND_COL_HEIGHT * i),
        )

    # left zone
    for i in range(ZONE_COLS + 1):
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_LEFT_TOP_X + LAND_COL_WIDTH * i, LAND_LEFT_TOP_Y),
                        (LAND_LEFT_BOTTOM_X + LAND_COL_WIDTH * i, LAND_LEFT_BOTTOM_Y),
        )

    # mid zone
    for i in range(ZONE_COLS + 1):
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_MID_TOP_X + LAND_COL_WIDTH * i, LAND_MID_TOP_Y),
                        (LAND_MID_BOTTOM_X + LAND_COL_WIDTH * i, LAND_MID_BOTTOM_Y),
        )

    # right zone
    for i in range(ZONE_COLS + 1):
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_RIGHT_TOP_X + LAND_COL_WIDTH * i, LAND_RIGHT_TOP_Y),
                        (LAND_RIGHT_BOTTOM_X + LAND_COL_WIDTH * i, LAND_RIGHT_BOTTOM_Y),
        )

    for zone in [ZONE_LEFT, ZONE_RIGHT, ZONE_MID]:
        for col in range(ZONE_COLS):
            for row in range(ZONE_ROWS):
                coord = getCenter(zone, (col, row))
                pygame.draw.rect(surface, (0xFF, 0xFF, 0xFF), coord + (1, 1))
                

def drawLandscape(surface: pygame.Surface):
    pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                     (LAND_X, LAND_Y),
                     (LAND_X + LAND_WIDTH, LAND_Y),
    )
    # This line should be just above the top edge of the player/enemy list dialogs.
    pygame.draw.line(surface, (0xFF, 0, 0xFF),
                     (LAND_X, LAND_Y + LAND_HEIGHT - 1 - lib.dialog.BORDER_HEIGHT),
                     (LAND_X + LAND_WIDTH, LAND_Y + LAND_HEIGHT - 1 - lib.dialog.BORDER_HEIGHT),
    )
    drawZones(surface)

class BattleFighter():
    def __self__(self, side: SideNo, zone: ZoneNo, fighter: lib.fighter.Fighter, brect: tuple[int, int, int, int]):
        lib.grid.checkBounds(brect, (ZONE_COLS, ZONE_ROWS))
        self.side = side
        self.zone = zone
        self.fighter = fighter
        self.brect = brect

class Battle():
    def __init__(self):
        self.fighters = []
        self.enemyList = lib.dialog.Dialog(lib.dialog.posEnemyList())
        self.playerList = lib.dialog.Dialog(lib.dialog.posPlayerList())

    # brect encodes position and size of the fighter.
    def addFighter(self, side: SideNo, zone: ZoneNo, fighter: lib.fighter.Fighter, brect: tuple[int, int, int, int]):
        self.fighters.append(BattleFighter(side, zone, fighter, brect))

    def giveInput(self, what):
        pass

    def tick(self):
        pass

    def render(self, surface: pygame.Surface):
        drawLandscape(surface)
        self.enemyList.render(surface)
        self.playerList.render(surface)
