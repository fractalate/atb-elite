import model.battle
import model.stats

class CalcAttack:
    def __init__(self, fighter: 'model.battle.ModelBattleFighter', target: 'model.battle.ModelBattleFighter'):
        # XXX: A provisional damage calculation. This will be a lot more intensive when all things are considered.
        self.damage: int = max(0, round((fighter.offense + fighter.damage.physical) * 3 - (target.defense + target.resist.physical) * 1.5))
