from model import BattleFieldCell, ZONE_LEFT, ZONE_MID, ZONE_RIGHT, ZONE_COLS, ZONE_ROWS

class BattleField:
    def __init__(self) -> None:
        self._cells: list[list[list[BattleFieldCell]]] = [
            [
                [[BattleFieldCell()
                    for _ in range(ZONE_ROWS)]]
                        for _ in range(ZONE_COLS)
            ] for _ in [
                ZONE_LEFT,
                ZONE_MID,
                ZONE_RIGHT,
            ]
        ]

    def getCell(self, zone: int, col: int, row: int) -> BattleFieldCell:
        return self._cells[zone][col][row]

