import bisect

import pygame

import engine

BLACK = pygame.Color(0, 0, 0)

def secondsToFrames(seconds: float) -> int:
    return round(seconds * engine.FRAME_RATE)

pygame.init()

_screen: pygame.Surface = pygame.display.set_mode((engine.DISPLAY_WIDTH, engine.DISPLAY_HEIGHT))
engine.gridInit(_screen)

_clock = pygame.time.Clock()
_input: 'engine.Input' = engine.Input()

_entitiesInput: list[engine.Entity] = []
_entitiesTick: list[engine.Entity] = []
_entitiesRender: list[engine.Entity] = []

def add(entity: engine.Entity):
    if entity.mode & engine.Entity.MODE_INPUT:
        bisect.insort_right(_entitiesInput, entity, key = lambda entity: entity.z)
    if entity.mode & engine.Entity.MODE_TICK:
        bisect.insort_right(_entitiesTick, entity, key = lambda entity: entity.z)
    if entity.mode & engine.Entity.MODE_RENDER:
        bisect.insort_right(_entitiesRender, entity, key = lambda entity: entity.z)

def remove(entity: engine.Entity):
    if entity in _entitiesInput:
        _entitiesInput.remove(entity)
    if entity in _entitiesTick:
        _entitiesTick.remove(entity)
    if entity in _entitiesRender:
        _entitiesRender.remove(entity)
    entity.cleanup()

def run():
    running = True
    entitiesRemove: list[engine.Entity] = []
    while running:
        # --- EVENT HANDLING ---------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        # --- INPUT HANDLING ---------------------------------------------------

        for event in _input.tick():
            for entity in _entitiesInput:
                if entity.giveInput(event):
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

        _clock.tick(engine.FRAME_RATE)
