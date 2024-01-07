from model import Clocked, Battle

class Status(Clocked):
    @staticmethod
    def isStatusStop(status: 'Status') -> bool:
        from model import StatusStop # XXX: Avoiding circular imports.
        return isinstance(status, StatusStop)

    @staticmethod
    def isStatusConfuse(status: 'Status') -> bool:
        from model import StatusConfuse # XXX: Avoiding circular imports.
        return isinstance(status, StatusConfuse)

    def __init__(self, ticks: int, due: int = 0) -> None:
        Clocked.__init__(self, ticks, due = due)
