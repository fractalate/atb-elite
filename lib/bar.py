import pygame

import lib.grid

class ProgressBar():
    def __init__(self, limit: int, grect: tuple[int, int, int, int]):
        self.grect = grect
        self.limit = limit
        self.value = 0

    def giveInput(self):
        pass

    def tick(self):
        pass

    def render(self, surface: pygame.Surface):
        x, y = lib.grid.toScreen(self.grect[0:2])
        width, height = lib.grid.toScreen(self.grect[2:4])
        height -= lib.grid.GRID_STEP_Y // 2
        y += lib.grid.GRID_STEP_Y // 4
        pygame.draw.rect(surface, (0x00, 0x00, 0x00), (x, y, width, height))
        if self.value > 0:
            fillPercent = self.value / self.limit
            fillWidth = fillPercent * width
            pygame.draw.rect(surface, (0x11, 0xAB, 0x33), (x, y, fillWidth, height))
