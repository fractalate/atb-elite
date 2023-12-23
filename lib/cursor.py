import pygame

import lib.input
import lib.grid
import lib.text

CURSOR = lib.text.RenderText((1, 1), '>')

class CursorSelector():
    def __init__(self, count):
        self.count = count
        self.position = 0

    def giveInput(self, what):
        if what == lib.input.UP:
            if self.position > 0:
                self.position -= 1
        elif what == lib.input.DOWN:
            if self.position < self.count - 1:
                self.position += 1

    def tick(self):
        pass

    def render(self, surface: pygame.Surface, gcoord: tuple[int, int]):
        x, y = gcoord
        y += self.position
        CURSOR.render(surface, (x, y))
