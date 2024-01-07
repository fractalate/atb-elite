from model import StatsDamage

class StatsBase:
    def __init__(self):
        self.hp: int = 0
        self.hp_max: int = 0
        self.mp: int = 0
        self.mp_max: int = 0
        self.pp: int = 0
        self.pp_max: int = 0

        self.speed: int = 0
        self.move: int = 0
        self.luck: int = 0

        self.offense: int = 0
        self.defense: int = 0
        self.psychic: int = 0

        self.damage: StatsDamage = StatsDamage()
        self.resist: StatsDamage = StatsDamage()
