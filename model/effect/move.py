import model

class EffectMove(model.Effect):
    def __init__(self, fighter: model.Fighter, coord: tuple[int, int]) -> None:
        model.Effect.__init__(self)
        self.fighter: model.Fighter = fighter
        self.coord: tuple[int, int] = coord

    def apply(self, battle: model.Battle) -> None:
        self.fighter.zoneX, self.fighter.zoneY = self.coord

