from model import Battle, Status
from model import TICK_RATE

TICKS_STATUS_STOP: int = TICK_RATE * 10

class StatusStop(Status):
    def __init__(self, battle: Battle) -> None:
        Status.__init__(self, battle, TICKS_STATUS_STOP)
