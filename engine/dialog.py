import pygame

import engine


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

class Dialog(engine.Entity):
    def __init__(self, grect: pygame.Rect, text: str) -> None:
        engine.Entity.__init__(self, mode = engine.Entity.MODE_INPUT | engine.Entity.MODE_RENDER)
        self.rect: pygame.Rect = engine.gridRectToScreen(grect)
        self.gcoord: tuple[int, int] = (grect.x, grect.y)
        self.text: engine.BasicText = engine.BasicText((grect.w, grect.h), text)

    def giveInput(self, event: engine.InputEvent) -> bool | None:
        if event == engine.CONFIRM:
            self.frames = 1 # XXX: Causes the dialog entity to be removed.
        return True

    def render(self, surface: pygame.Surface) -> None:
        # TODO: Turn colors into globals.
        pygame.draw.rect(surface, (0x11, 0x0B, 0xC4), self.rect)
        rect = _growRect(self.rect)
        drawRectLines(surface, rect, (0xBB, 0xBB, 0xBB))
        rect = _growRect(rect)
        drawRectLines(surface, rect, (0xFF, 0xFF, 0xFF))
        self.text.render(surface, self.gcoord)

# XXX: Probably a temporary thing.
class DialogQuick(Dialog):
    def __init__(self, grect: pygame.Rect, text: str) -> None:
        Dialog.__init__(self, grect, text)
        self.frames = 100
