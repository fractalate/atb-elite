import pygame

import textwrap

import engine

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
    BORDER_WIDTH = 2
    BORDER_HEIGHT = 2

    def __init__(self, grect: pygame.Rect, text: None | str = None) -> None:
        engine.Entity.__init__(self, mode = engine.Entity.MODE_INPUT | engine.Entity.MODE_RENDER)
        self.rect: pygame.Rect = engine.gridRectToScreen(grect)
        self.grect: pygame.Rect = grect.copy()
        self.text: None | engine.BasicText = None
        if text is not None:
            self.setText(text)

    def setText(self, text: None | str) -> str:
        if text is None:
            self.text = None
        else:
            self.text = engine.BasicText((self.grect.w, self.grect.h), text)

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
        if self.text is not None:
            self.text.render(surface, (self.grect.x, self.grect.y))

# XXX: Probably a temporary thing.
class DialogQuick(Dialog):
    def __init__(self, grect: pygame.Rect, text: str) -> None:
        Dialog.__init__(self, grect, '\n'.join(textwrap.wrap(text, 20)))
        self.frames = 100
