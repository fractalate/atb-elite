import model.battle

class KO(model.battle.Effect):
    def __init__(self, fighter: model.battle.Fighter) -> None:
        model.battle.Effect.__init__(self)
        self.fighter: model.battle.Fighter = fighter

