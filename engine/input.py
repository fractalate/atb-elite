from typing import Generator

import pygame

import engine.sys

class What(int): pass

UP: What = 0
DOWN: What = 1
LEFT: What = 2
RIGHT: What = 3

CONFIRM: What = 4 # ><
CANCEL: What = 5  # ()
MENU: What = 6    # /\
ACTION: What = 7  # []

START: What = 8
SELECT: What = 9

DEBUG1: What = 33
DEBUG2: What = 34
DEBUG3: What = 35
DEBUG4: What = 36
DEBUG5: What = 37
DEBUG6: What = 38

# Desired to feel like you've held the button for emphasis with the intention of repeating.
TICKS_HOLD = engine.sys.FRAME_RATE // 2
# Desired to be quite rapid feeling.
TICKS_HOLD_REPEAT = engine.sys.FRAME_RATE // 16

class InputState():
    def __init__(self) -> None:
        self.state: int = 0

    # Returns true if this input is triggered and should send.
    #
    # When pressed:
    #
    #  start                  -1 -> -2 -> ... -> -TICKS_HOLD_REPEAT-1
    #    |                     ^                          |
    #   <x>                    |                          |
    #    |                    <x>-------------------------+
    #    v                     |
    #    0 -> 1 -> ... -> TICKS_HOLD
    #
    def tick(self, pressed: bool) -> bool:
        result = False
        if pressed:
            if self.state == 0:
                result = True
                self.state += 1
            elif self.state > 0:
                self.state += 1
                if self.state > TICKS_HOLD:
                    self.state = -1
                    result = True
            else:
                self.state -= 1
                if self.state < -TICKS_HOLD_REPEAT - 1:
                    self.state = -1
                    result = True
        else:
            self.state = 0
        return result

class Input():
    def __init__(self) -> None:
        self.key_up: InputState = InputState()
        self.key_down: InputState = InputState()
        self.key_left: InputState = InputState()
        self.key_right: InputState = InputState()

        self.key_confirm: InputState = InputState()
        self.key_cancel: InputState = InputState()
        self.key_menu: InputState = InputState()
        self.key_action: InputState = InputState()

        self.key_start: InputState = InputState()
        self.key_select: InputState = InputState()

        self.debug1: InputState = InputState()
        self.debug2: InputState = InputState()
        self.debug3: InputState = InputState()
        self.debug4: InputState = InputState()
        self.debug5: InputState = InputState()
        self.debug6: InputState = InputState()

    def tick(self) -> Generator[What, None, None]:
        pressed = pygame.key.get_pressed()

        if self.key_up.tick(pressed[pygame.K_UP]):
            yield UP
        if self.key_down.tick(pressed[pygame.K_DOWN]):
            yield DOWN
        if self.key_left.tick(pressed[pygame.K_LEFT]):
            yield LEFT
        if self.key_right.tick(pressed[pygame.K_RIGHT]):
            yield RIGHT

        if self.key_confirm.tick(pressed[pygame.K_SPACE]):
            yield CONFIRM
        if self.key_cancel.tick(pressed[pygame.K_ESCAPE]):
            yield CANCEL
        if self.key_menu.tick(pressed[pygame.K_PAGEUP]):
            yield MENU
        if self.key_action.tick(pressed[pygame.K_BACKQUOTE]):
            yield ACTION

        if self.key_start.tick(pressed[pygame.K_RETURN]):
            yield START
        if self.key_select.tick(pressed[pygame.K_BACKSPACE]):
            yield SELECT

        if self.debug1.tick(pressed[pygame.K_F1]):
            yield DEBUG1
        if self.debug2.tick(pressed[pygame.K_F2]):
            yield DEBUG2
        if self.debug3.tick(pressed[pygame.K_F3]):
            yield DEBUG3
        if self.debug4.tick(pressed[pygame.K_F4]):
            yield DEBUG4
        if self.debug5.tick(pressed[pygame.K_F5]):
            yield DEBUG5
        if self.debug6.tick(pressed[pygame.K_F6]):
            yield DEBUG6
