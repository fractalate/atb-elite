from model import Action
from model import TICK_RATE

TICKS_ACTION_MOVE: int = round(TICK_RATE * .75)

class ActionMove(Action):
    def __init__(self) -> None:
        Action.__init__(self)
