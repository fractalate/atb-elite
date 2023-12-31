import model.battle

class Poison(model.battle.Status):
    def __init__(self) -> None:
        model.battle.Status.__init__(self, ticksLimit = round(model.battle.TICK_RATE * 10))
