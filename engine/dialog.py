import pygame

import engine.grid
import engine.text

BORDER_WIDTH = BORDER_HEIGHT = 2

# XXX: Remove if not useful.
def shrinkRect(rect: pygame.Rect):
    x, y, width, height = rect
    return x + 1, y + 1, width - 2, height - 2

def growRect(rect: pygame.Rect):
    x, y, width, height = rect
    return x - 1, y - 1, width + 2, height + 2

def drawRectLines(surface: pygame.Surface, rect: pygame.Rect, color: pygame.Color):
    x, y, width, height = rect
    closed = True
    pygame.draw.lines(surface, color, closed, [
      (x, y),
      (x + width - 1, y),
      (x + width - 1, y + height - 1),
      (x, y + height - 1),
    ])

class Dialog():
    def __init__(self, grect: tuple[int, int, int, int]):
        self.grect = grect
        x, y = engine.grid.toScreen(grect[0:2])
        width, height = engine.grid.toScreen(grect[2:4])
        self.rect = (x, y, width, height)
        self.text = None
        # XXX: Not sure of the function type hint. It should be a () -> void in TypeScript notation.
        self.inputHandlers: dict[str, list[function]] = dict()

    def setText(self, text: str):
        self.text = engine.text.RenderText(self.grect[2:4], text)
        return self

    def addInputHandler(self, what, callback):
        if what in self.inputHandlers:
            self.inputHandlers[what].append(callback)
        else:
            self.inputHandlers[what] = [callback]
        return self

    def giveInput(self, what):
        if what in self.inputHandlers:
            for handler in self.inputHandlers[what]:
                handler()

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0x11, 0x0B, 0xC4), self.rect)
        rect = growRect(self.rect)
        drawRectLines(surface, rect, (0xBB, 0xBB, 0xBB))
        rect = growRect(rect)
        drawRectLines(surface, rect, (0xFF, 0xFF, 0xFF))
        if self.text is not None:
            self.text.render(surface, self.grect[0:2])

def posEnemyList():
    return (0, 20, 18, 4)

def sizeEnemyNameInEnemyList():
    return (18, 1)

def posPlayerList():
    return (18, 20, 14, 4)

def sizePlayerNameInPlayerList():
    return (6, 1)
