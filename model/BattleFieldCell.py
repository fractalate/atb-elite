class BattleFieldCell:
    NORMAL = 0
    IMPASSIBLE = 1

    def __init__(self) -> None:
        self.state: int = BattleFieldCell.NORMAL
