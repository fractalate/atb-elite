import pygame

import engine

class Entity:
    MODE_INPUT:  int = 0b001
    MODE_TICK:   int = 0b010
    MODE_RENDER: int = 0b100

    def __init__(self, mode: int = 0, ticks: int = 0, frames: int = 0, z: int = 0) -> None:
        self.mode: int = mode
        self.ticks: int = ticks
        self.frames: int = frames
        self.z: int = z

        # XXX: Sanity checks. Maybe I should use the same counter for both cases?
        if mode & Entity.MODE_TICK and mode & Entity.MODE_RENDER == 0 and self.frames != 0:
            raise AssertionError('MODE_TICK entity has frames set (did you mean to set ticks instead?)')
        if mode & Entity.MODE_RENDER and mode & Entity.MODE_TICK == 0 and self.ticks != 0:
            raise AssertionError('MODE_RENDER entity has frames set (did you mean to set frames instead?)')

    def giveInput(self, event: engine.InputEvent) -> None | bool:
        pass

    def tick(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

    def cleanup(self) -> None:
        pass
