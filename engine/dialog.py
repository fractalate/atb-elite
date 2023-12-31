import pygame

import engine.grid
import engine.text

BORDER_WIDTH = BORDER_HEIGHT = 2

def _growRect(rect: pygame.Rect) -> pygame.Rect:
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
    def __init__(self, grect: pygame.Rect) -> None:
        self.grect: pygame.Rect = grect # XXX: Candidate for removal.
        self.rect: pygame.Rect = engine.grid.rectToScreen(grect)

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (0x11, 0x0B, 0xC4), self.rect)
        rect = _growRect(self.rect)
        drawRectLines(surface, rect, (0xBB, 0xBB, 0xBB))
        rect = _growRect(rect)
        drawRectLines(surface, rect, (0xFF, 0xFF, 0xFF))
