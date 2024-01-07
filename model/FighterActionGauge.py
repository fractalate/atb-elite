class FighterActionGauge:
    def __init__(self) -> None:
        self.value: int = 0
        self.limit: int = 0

    def reset(self) -> None:
        self.value = 0

    def isFull(self) -> bool:
        return self.value >= self.limit

    def increment(self) -> None:
        if self.value < self.limit:
            self.value += 1
