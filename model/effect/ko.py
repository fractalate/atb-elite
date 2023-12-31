import model

class EffectKO(model.Effect):
    def __init__(self, fighter: model.Fighter) -> None:
        model.Effect.__init__(self)
        self.fighter: model.Fighter = fighter

