from model import Fighter

class CalcMagicFireDamage:
    def __init__(self, fighter: Fighter, target: Fighter) -> None:
        self.fighter: Fighter = fighter
        self.target: Fighter = target
        self.damage: int = 100 # TODO
