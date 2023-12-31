""" ---  --- """
# XXX: Maybe there's another way to do this?
# XXX: I'd also like to put the window at the position it was in for the last
#      run, but it seems like this requires usage of some unrelated libraries
#      and might not be easy to make it cross platform. The basic idea I would
#      want to implement is to save the window position at shutdown, then
#      restore it at startup only if the window would be fully in the display.
#      Otherwise start at (0, 0).
import os
# For setting the window position when starting up. This needs to be done
# before pygame.display.set_mode().
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1528, 0)
""" ---  --- """

""" ---  --- """
# XXX: Pre-emptive initialization so it's ready for lib.text. Maybe do it early
#      in there instead?
import pygame
pygame.init()
""" ---  --- """

import bisect

import pygame

import engine.grid
import engine.input
import engine.sys

BLACK = pygame.Color(0, 0, 0)

def secondsToFrames(seconds: float) -> int:
    return round(seconds * engine.sys.FRAME_RATE)

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

    def giveInput(self, what: engine.input.What) -> None | bool:
        pass

    def tick(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

pygame.init()

_screen = pygame.display.set_mode((engine.sys.DISPLAY_WIDTH, engine.sys.DISPLAY_HEIGHT))
engine.grid.init(_screen)

_clock = pygame.time.Clock()
_input: 'engine.input.Input' = engine.input.Input()

_entitiesInput: list[Entity] = []
_entitiesTick: list[Entity] = []
_entitiesRender: list[Entity] = []

def add(entity: Entity):
    if entity.mode & Entity.MODE_INPUT:
        bisect.insort_right(_entitiesInput, entity, key = lambda entity: entity.z)
    if entity.mode & Entity.MODE_TICK:
        bisect.insort_right(_entitiesTick, entity, key = lambda entity: entity.z)
    if entity.mode & Entity.MODE_RENDER:
        bisect.insort_right(_entitiesRender, entity, key = lambda entity: entity.z)

def remove(entity: Entity):
    if entity in _entitiesInput:
        _entitiesInput.remove(entity)
    if entity in _entitiesTick:
        _entitiesTick.remove(entity)
    if entity in _entitiesRender:
        _entitiesRender.remove(entity)

def run():
    running = True
    entitiesRemove: list[Entity] = []
    while running:
        # --- EVENT HANDLING ---------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        # --- INPUT HANDLING ---------------------------------------------------

        for what in _input.tick():
            for entity in _entitiesInput:
                if entity.giveInput(what):
                    break

        # --- TICK -------------------------------------------------------------

        for entity in _entitiesTick:
            entity.tick()
            if entity.ticks > 0:
                entity.ticks -= 1
                if entity.ticks == 0:
                    entitiesRemove.append(entity)

        if entitiesRemove:
            for entity in entitiesRemove:
                remove(entity)
            entitiesRemove.clear()

        # --- RENDER -----------------------------------------------------------

        _screen.fill(BLACK)
        for entity in _entitiesRender:
            entity.render(_screen)
            if entity.frames > 0:
                entity.frames -= 1
                if entity.frames == 0:
                    entitiesRemove.append(entity)

        pygame.display.flip()

        if entitiesRemove:
            for entity in entitiesRemove:
                remove(entity)
            entitiesRemove.clear()

        # --- WAIT -------------------------------------------------------------

        _clock.tick(engine.sys.FRAME_RATE)
