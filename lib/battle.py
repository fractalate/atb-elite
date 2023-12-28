import pygame

import lib.bar
import lib.dialog
import lib.fighter
import lib.grid
import lib.sys
import lib.text

# XXX: Is there a better way to name simple types for type hinting?
FactionNo = int
ZoneNo = str # ZONE_LEFT, ZONE_RIGHT, ZONE_MID

# Player's faction is faction 0.
FACTION_PLAYER = 0
# All other fighters' factions are 1 or greater. Typically, it's 1.
FACTION_OTHER = 1

ZONE_LEFT = 'left'
ZONE_RIGHT = 'right'
ZONE_MID = 'mid'

ZONE_COLS = 3
ZONE_ROWS = 4 # This value is not really changeable. Use 4 to match the party size.

# Piggy backing on the grid system to lay out the battle zones' land.
HALF_X, HALF_Y = lib.grid.toScreen((1, 1))
HALF_X, HALF_Y = (HALF_X // 2, HALF_Y // 2)
LAND_X, LAND_Y = lib.grid.toScreen((0, 10))
LAND_WIDTH, LAND_HEIGHT = lib.grid.toScreen((32, 10))
LAND_LEFT_TOP_X, LAND_LEFT_TOP_Y = lib.grid.toScreen((3, 10))
LAND_LEFT_BOTTOM_X, LAND_LEFT_BOTTOM_Y = lib.grid.toScreen((0, 20))
LAND_RIGHT_TOP_X, LAND_RIGHT_TOP_Y = lib.grid.toScreen((23, 10))
LAND_RIGHT_BOTTOM_X, LAND_RIGHT_BOTTOM_Y = lib.grid.toScreen((26, 20))
LAND_MID_TOP_X, LAND_MID_TOP_Y = lib.grid.toScreen((13, 10))
LAND_MID_BOTTOM_X, LAND_MID_BOTTOM_Y = lib.grid.toScreen((13, 20))
LAND_COL_WIDTH, LAND_COL_HEIGHT = lib.grid.toScreen((2, 2))
LAND_COL_WIDTH, LAND_COL_HEIGHT = (LAND_COL_WIDTH, LAND_COL_HEIGHT + HALF_Y)

def getCenter(zone, cell: tuple[int, int]):
    # XXX: These were thrown together without lot of care. It's probably better to rewrite if extensive work is needed.
    if zone == ZONE_LEFT:
        col, row = cell
        x_shift = (LAND_LEFT_TOP_X - LAND_LEFT_BOTTOM_X) * (ZONE_ROWS - row - 1) // ZONE_ROWS + HALF_X
        return (
            LAND_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 + x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == ZONE_RIGHT:
        col, row = cell
        x_shift = (LAND_RIGHT_TOP_X - LAND_RIGHT_BOTTOM_X) * (row) // ZONE_ROWS - HALF_X
        return (
            LAND_RIGHT_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2 - x_shift,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    elif zone == ZONE_MID:
        col, row = cell
        return (
            LAND_MID_TOP_X + col * LAND_COL_WIDTH + LAND_COL_WIDTH // 2,
            LAND_Y + row * LAND_COL_HEIGHT + LAND_COL_HEIGHT // 2,
        )
    return lib.grid.toScreen(cell)

def cellToScreen(zone, cell: tuple[int, int]):
    col, row = cell
    if zone == ZONE_LEFT:
        x = LAND_LEFT_TOP_X + col * LAND_COL_WIDTH
        x += (LAND_LEFT_TOP_X - LAND_LEFT_BOTTOM_X) * (ZONE_ROWS - row - 4) // ZONE_ROWS
        y = LAND_LEFT_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    elif zone == ZONE_RIGHT:
        x = LAND_RIGHT_TOP_X + col * LAND_COL_WIDTH
        x -= (LAND_RIGHT_TOP_X - LAND_RIGHT_BOTTOM_X) * row // ZONE_ROWS
        y = LAND_RIGHT_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    elif zone == ZONE_MID:
        x = LAND_MID_TOP_X + col * LAND_COL_WIDTH
        y = LAND_MID_TOP_Y + row * LAND_COL_HEIGHT
        return (x, y)
    return cell # XXX: Maybe throw an error?

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

def drawZones(surface: pygame.Surface):
    for i in range(ZONE_ROWS):
        # Horizontal line for each cell.
        pygame.draw.line(surface, (0xFF, 0xFF, 0xFF),
                        (LAND_X, LAND_Y + LAND_COL_HEIGHT * i),
                        (LAND_X + LAND_WIDTH, LAND_Y + LAND_COL_HEIGHT * i),
        )

    for i in range(ZONE_COLS + 1):
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
    for zone in [ZONE_LEFT, ZONE_RIGHT, ZONE_MID]:
        for col in range(ZONE_COLS):
            for row in range(ZONE_ROWS):
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
                     (LAND_X, LAND_Y + LAND_HEIGHT - 1 - lib.dialog.BORDER_HEIGHT),
                     (LAND_X + LAND_WIDTH, LAND_Y + LAND_HEIGHT - 1 - lib.dialog.BORDER_HEIGHT),
    )
    drawZones(surface)

def calculateFramesForSpd(spd):
    spd = min(spd, 255)
    return max(1, round((300 - spd + 1) / 60 * lib.sys.FRAME_RATE))

class BattleFighter():
    def __init__(self, faction: FactionNo, zone: ZoneNo, name: str, fighter: lib.fighter.Fighter, cells: tuple[int, int, int, int]):
        lib.grid.checkBounds(cells, (ZONE_COLS, ZONE_ROWS))
        self.faction = faction
        self.zone = zone
        self.name = name
        self.fighter = fighter
        self.cells = cells
        if faction == FACTION_PLAYER:
            self.bar = lib.bar.ProgressBar(calculateFramesForSpd(fighter.spd))
            self.nameText = lib.text.PalletteText(lib.dialog.sizePlayerNameInPlayerList(), self.name)
        else:
            self.bar = None
            self.nameText = lib.text.PalletteText(lib.dialog.sizeEnemyNameInEnemyList(), self.name)

class Battle():
    def __init__(self):
        self.fighters: list[BattleFighter] = []
        self.playerCounter = 0
        self.playerActionQueue: list[BattleFighter] = []
        self.enemyList = lib.dialog.Dialog(lib.dialog.posEnemyList())
        self.playerList = lib.dialog.Dialog(lib.dialog.posPlayerList())

    def addFighter(self, faction: FactionNo, zone: ZoneNo, name: str, fighter: lib.fighter.Fighter, cells: tuple[int, int, int, int]):
        self.fighters.append(BattleFighter(faction, zone, name, fighter, cells))

    def giveInput(self, what):
        pass

    def tick(self):
        for fighter in self.fighters:
            if fighter.faction == FACTION_PLAYER:
                if fighter.bar.value < fighter.bar.limit:
                    fighter.bar.value += 1
                elif fighter not in self.playerActionQueue:
                    self.playerActionQueue.append(fighter)

    def render(self, surface: pygame.Surface):
        ### --- Render Scene ----------------------------------------------- ###

        drawLandscape(surface)

        ### --- Render Fighters -------------------------------------------- ###

        for fighter in self.fighters:
            if fighter.faction == FACTION_PLAYER:
                color = (0x11, 0x88, 0x22)
            else:
                color = (0x88, 0x22, 0x11)
            drawCellsBorder(surface, fighter.zone, fighter.cells, color = color)

        ### --- Render Enemy List ------------------------------------------ ###

        self.enemyList.render(surface)
        otherFighterNo = 0
        for fighter in self.fighters:
            if fighter.faction != FACTION_PLAYER:
                col, row, _, height = lib.dialog.posEnemyList()
                nameWidth, _ = lib.dialog.sizeEnemyNameInEnemyList()
                if otherFighterNo < height:
                    fighter.nameText.render(surface, (col, row + otherFighterNo))
                    otherFighterNo += 1

        ### --- Render Player List ----------------------------------------- ###

        self.playerList.render(surface)
        playerFighterNo = 0
        for fighter in self.fighters:
            if fighter.faction == FACTION_PLAYER:
                col, row, _, _ = lib.dialog.posPlayerList()
                if fighter.fighter.hp == 0:
                    pallette = lib.text.PALLETTE_RED # Red - Dead.
                elif self.playerActionQueue and fighter is self.playerActionQueue[0]:
                    pallette = lib.text.PALLETTE_YELLOW # Yellow - Current acting player fighter.
                else:
                    pallette = lib.text.PALLETTE_WHITE # White - Otherwise.
                fighter.nameText.render(surface, (col, row + playerFighterNo), pallette)
                hp = lib.text.pad(str(fighter.fighter.hp), 4)
                nameWidth, _ = lib.dialog.sizePlayerNameInPlayerList()
                lib.text.renderDigits(surface, (col + nameWidth + 1, row + playerFighterNo, 4, 1), hp, pallette = pallette)
                fighter.bar.render(surface, (col + nameWidth + 1 + 4, row + playerFighterNo, 3, 1))
                playerFighterNo += 1
