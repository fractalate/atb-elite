from model import Effect, Fighter

class EffectKO(Effect):
    def __init__(self, fighter: Fighter) -> None:
        Effect.__init__(self)
        self.fighter = fighter

    def apply(self) -> None:
        pass
