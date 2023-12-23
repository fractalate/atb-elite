import pygame

import lib.sys

# XXX: Replace these with int values eventually.
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
CONFIRM = 'Confirm'
CANCEL = 'Cancel'

# Desired to feel like you've held the button for emphasis with the intention of repeating.
TICKS_HOLD = lib.sys.FRAME_RATE // 2
# Desired to be quite rapid feeling.
TICKS_HOLD_REPEAT = lib.sys.FRAME_RATE // 16

class InputState():
    def __init__(self):
        self.state = 0

    # Returns true if this input is triggered and should send.
    def tick(self, pressed):
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
    def __init__(self):
        self.key_up = InputState()
        self.key_down = InputState()
        self.key_left = InputState()
        self.key_right = InputState()
        self.key_confirm = InputState()
        self.key_cancel = InputState()

    def tick(self):
        pressed = pygame.key.get_pressed()
        if self.key_up.tick(pressed[pygame.K_UP]):
            yield UP
        if self.key_down.tick(pressed[pygame.K_DOWN]):
            yield DOWN
        if self.key_left.tick(pressed[pygame.K_LEFT]):
            yield LEFT
        if self.key_right.tick(pressed[pygame.K_RIGHT]):
            yield RIGHT
        if self.key_cancel.tick(pressed[pygame.K_ESCAPE]):
            yield CANCEL
        if self.key_confirm.tick(pressed[pygame.K_RETURN]):
            yield CONFIRM
