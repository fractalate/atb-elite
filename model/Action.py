from model import Clocked

class Action(Clocked):
    MODE_ACTIVE = 0
    MODE_PAUSE = 1

    def __init__(self, ticks: int, due: int = 0, mode: int = MODE_ACTIVE) -> None:
        Clocked.__init__(self, ticks, due = due)
        self.mode: int = mode

    # Check if this action is possible to perform.
    def isPossible(self) -> bool:
        return False
