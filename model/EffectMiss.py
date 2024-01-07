from model import Effect, Fighter

class EffectMiss(Effect):
    def __init__(self, fighter: Fighter, target: Fighter) -> None:
        Effect.__init__(self)
        self.fighter: Fighter = fighter
        self.target: Fighter = target
