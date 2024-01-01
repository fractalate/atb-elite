import pygame

import engine

import model

# Piggy backing on the grid system to lay out the battle zones' land.
HALF_X, HALF_Y = engine.gridCoordToScreen((1, 1))
HALF_X, HALF_Y = (HALF_X // 2, HALF_Y // 2)
LAND_X, LAND_Y = engine.gridCoordToScreen((0, 10))
LAND_WIDTH, LAND_HEIGHT = engine.gridCoordToScreen((32, 10))
LAND_LEFT_TOP_X, LAND_LEFT_TOP_Y = engine.gridCoordToScreen((3, 10))
LAND_LEFT_BOTTOM_X, LAND_LEFT_BOTTOM_Y = engine.gridCoordToScreen((0, 20))
LAND_RIGHT_TOP_X, LAND_RIGHT_TOP_Y = engine.gridCoordToScreen((23, 10))
LAND_RIGHT_BOTTOM_X, LAND_RIGHT_BOTTOM_Y = engine.gridCoordToScreen((26, 20))
LAND_MID_TOP_X, LAND_MID_TOP_Y = engine.gridCoordToScreen((13, 10))
LAND_MID_BOTTOM_X, LAND_MID_BOTTOM_Y = engine.gridCoordToScreen((13, 20))
LAND_COL_WIDTH, LAND_COL_HEIGHT = engine.gridCoordToScreen((2, 2))
LAND_COL_WIDTH, LAND_COL_HEIGHT = (LAND_COL_WIDTH, LAND_COL_HEIGHT + HALF_Y)

def getCenter(zone, cell: tuple[int, int]):
    # XXX: These were thrown together without lot of care. It's probably better to rewrite if extensive work is needed.
    if zone == model.ZONE_LEFT:
        col, row = cell
        x_shift = (LAND_LEFT_TOP_X - LAND_LEFT_BOTTOM_X) * (model.ZONE_ROWS - row - 1) // model.ZONE_ROWS + HALF_X
        return (
            LAND_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 + x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == model.ZONE_RIGHT:
        col, row = cell
        x_shift = (LAND_RIGHT_TOP_X - LAND_RIGHT_BOTTOM_X) * (row) // model.ZONE_ROWS - HALF_X
        return (
            LAND_RIGHT_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 - x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == model.ZONE_MID:
        col, row = cell
        return (
            LAND_MID_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    return engine.gridCoordToScreen(cell)

def cellToScreen(zone, cell: tuple[int, int]):
    col, row = cell
    if zone == model.ZONE_LEFT:
        x = LAND_LEFT_TOP_X + col * LAND_COL_WIDTH
        x += (LAND_LEFT_TOP_X - LAND_LEFT_BOTTOM_X) * (model.ZONE_ROWS - row - 4) // model.ZONE_ROWS
        y = LAND_LEFT_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    elif zone == model.ZONE_RIGHT:
        x = LAND_RIGHT_TOP_X + col * LAND_COL_WIDTH
        x -= (LAND_RIGHT_TOP_X - LAND_RIGHT_BOTTOM_X) * row // model.ZONE_ROWS
        y = LAND_RIGHT_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    elif zone == model.ZONE_MID:
        x = LAND_MID_TOP_X + col * LAND_COL_WIDTH
        y = LAND_MID_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    return cell # XXX: Maybe throw an error?

def drawZones(surface: pygame.Surface):
    for i in range(model.ZONE_ROWS):
        # Horizontal line for each cell.
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_X, LAND_Y + LAND_COL_HEIGHT * i),
                        (LAND_X + LAND_WIDTH, LAND_Y + LAND_COL_HEIGHT * i),
        )

    for i in range(model.ZONE_COLS + 1):
        # Left zone cell vertical line.
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_LEFT_TOP_X + LAND_COL_WIDTH * i, LAND_LEFT_TOP_Y),
                        (LAND_LEFT_BOTTOM_X + LAND_COL_WIDTH * i, LAND_LEFT_BOTTOM_Y),
        )
        # Mid zone cell vertical line.
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_MID_TOP_X + LAND_COL_WIDTH * i, LAND_MID_TOP_Y),
                        (LAND_MID_BOTTOM_X + LAND_COL_WIDTH * i, LAND_MID_BOTTOM_Y),
        )
        # Right zone cell vertical line.
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_RIGHT_TOP_X + LAND_COL_WIDTH * i, LAND_RIGHT_TOP_Y),
                        (LAND_RIGHT_BOTTOM_X + LAND_COL_WIDTH * i, LAND_RIGHT_BOTTOM_Y),
        )

    # Points at the center of each zone cell.
    for zone in [model.ZONE_LEFT, model.ZONE_RIGHT, model.ZONE_MID]:
        for col in range(model.ZONE_COLS):
            for row in range(model.ZONE_ROWS):
                coord = getCenter(zone, (col, row))
                # XXX: Draws a point. Is there a dedicated point function I can use?
                pygame.draw.rect(surface, (0xFF, 0xFF, 0xFF), coord + (1, 1))

def drawLandscape(surface: pygame.Surface):
    # Horizon line.
    pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                     (LAND_X, LAND_Y),
                     (LAND_X + LAND_WIDTH, LAND_Y),
    )
    # Bottom boundary line. This line should be just above the top edge of the player/enemy list dialogs.
    # XXX: Useful for debugging. Remove later to offer the full field for the graphics.
    pygame.draw.line(surface, (0xFF, 0, 0xFF),
                     (LAND_X, LAND_Y + LAND_HEIGHT - 1 - engine.Dialog.BORDER_HEIGHT),
                     (LAND_X + LAND_WIDTH, LAND_Y + LAND_HEIGHT - 1 - engine.Dialog.BORDER_HEIGHT),
    )
    drawZones(surface)

class Backdrop(engine.Entity):
    def __init__(self):
        engine.Entity.__init__(self, mode = engine.Entity.MODE_RENDER)

    def render(self, surface: pygame.Surface) -> None:
        drawLandscape(surface)

    @staticmethod
    def drawCellsBorder(surface: pygame.Surface, zone, cells: tuple[int, int, int, int], color = (0xFF, 0x00, 0xFF)):
        col, row, width, height = cells
        p0 = cellToScreen(zone, (col, row))
        p1 = cellToScreen(zone, (col + width, row))
        p2 = cellToScreen(zone, (col + width, row + height))
        p3 = cellToScreen(zone, (col, row + height))
        pygame.draw.line(surface, color, p0, p1)
        pygame.draw.line(surface, color, p1, p2)
        pygame.draw.line(surface, color, p2, p3)
        pygame.draw.line(surface, color, p3, p0)

