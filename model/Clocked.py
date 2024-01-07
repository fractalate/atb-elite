class Clocked:
    def __init__(self, ticks: int, due: int = 0) -> None:
        self.ticks: int = ticks
        self.due: int = due

    def isExpired(self) -> bool:
        return self.ticks <= 0

    def isTickDue(self) -> bool:
        return self.ticks <= 0 or self.ticks <= self.due

    def tick(self) -> None:
        pass
