import model.battle

DISPLAY_WIDTH: int = 1024
DISPLAY_HEIGHT: int = 768
TICK_RATE: int = model.battle.TICK_RATE
# XXX: Fix the frame rate to the tick rate, but I'd like to free the rendering framerate from the game ticks.
FRAME_RATE: int = TICK_RATE
