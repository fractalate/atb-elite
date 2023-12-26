import pygame

import lib.cursor
import lib.grid
import lib.text

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
        x, y = lib.grid.toScreen(grect[0:2])
        width, height = lib.grid.toScreen(grect[2:4])
        self.rect = (x, y, width, height)
        self.text = None
        self.selector = None
        self.selectorOffset = 0
        # XXX: Not sure of the function type hint. It should be a () -> void in TypeScript notation.
        self.inputHandlers: dict[str, list[function]] = dict()

    def setText(self, text: str):
        self.text = lib.text.RenderText(self.grect[2:4], text)
        return self

    # This function is not for mortals. Probably you want DialogPromptSelection().
    def setSelector(self, selector: lib.cursor.CursorSelector, selectorOffset = 0):
        self.selector = selector
        self.selectorOffset = selectorOffset
        return self

    def addInputHandler(self, what, callback):
        if what in self.inputHandlers:
            self.inputHandlers[what].append(callback)
        else:
            self.inputHandlers[what] = [callback]
        return self

    def giveInput(self, what):
        if self.selector is not None:
            self.selector.giveInput(what)
        if what in self.inputHandlers:
            for handler in self.inputHandlers[what]:
                handler()

    def tick(self):
        if self.selector is not None:
            self.selector.tick()

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0x11, 0x0B, 0xC4), self.rect)
        rect = growRect(self.rect)
        drawRectLines(surface, rect, (0xBB, 0xBB, 0xBB))
        rect = growRect(rect)
        drawRectLines(surface, rect, (0xFF, 0xFF, 0xFF))
        if self.text is not None:
            self.text.render(surface, self.grect[0:2])
        if self.selector is not None:
            x, y = self.grect[0:2]
            self.selector.render(surface, (x, y + self.selectorOffset))

def DialogPromptSelection(prompt: str, options: list[str], grect: tuple[int, int, int, int]):
    # XXX: If the full selection of items is not available, raise an error.
    lines = len(prompt.split('\n')) if prompt else 0
    for item in options:
        prompt += '\n ' + item
    # Skip initial \n from the first item if there is no prompt.
    if lines == 0:
        prompt = prompt[1:]
    dialog = Dialog(grect)
    dialog.setText(prompt)
    _, y, _, height = grect
    y += lines
    height -= lines
    height = min(len(options), height)
    dialog.setSelector(lib.cursor.CursorSelector(height), selectorOffset=lines)
    return dialog

class DialogStack():
    def __init__(self):
        self.stack: list[Dialog] = []

    def isCapturingInput(self):
        return len(self.stack) > 0

    def push(self, dialog: Dialog):
        self.stack.append(dialog)

    def remove(self, dialog: Dialog):
        self.stack.remove(dialog)

    def giveInput(self, what):
        if self.stack:
            self.stack[-1].giveInput(what)

    def tick(self):
        if self.stack:
            self.stack[-1].tick()

    def render(self, surface: pygame.Surface):
        for dialog in self.stack:
            dialog.render(surface)

def posEnemyList():
    return (0, 20, 18, 4)

def posPlayerList():
    return (18, 20, 14, 4)
