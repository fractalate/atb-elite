from model import Battle, Effect, Fighter

class EffectAddFighter(Effect):
    def __init__(self, battle: Battle, fighter: Fighter) -> None:
        Effect.__init__(self)
        self.battle: Battle = battle
        self.fighter: Fighter = fighter

    def apply(self) -> None:
        if self.fighter not in self.battle:
            self.battle.fighters.append(self.fighter)

