import model

class StatusPoison(model.Status):
    def __init__(self) -> None:
        model.Status.__init__(self, ticksLimit = round(model.TICK_RATE * 10))
