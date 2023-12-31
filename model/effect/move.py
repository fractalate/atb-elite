import model.battle

class Move(model.battle.Effect):
    def __init__(self, fighter: model.battle.Fighter, coord: tuple[int, int]) -> None:
        model.battle.Effect.__init__(self)
        self.fighter: model.battle.Fighter = fighter
        self.coord: tuple[int, int] = coord

    def apply(self, battle: model.battle.Battle) -> None:
        self.fighter.zoneX, self.fighter.zoneY = self.coord

