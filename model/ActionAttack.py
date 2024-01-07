from model import Action, Battle, CalcAttackDamage, EffectDamage, EffectMiss, Fighter
from model import TICK_RATE

TICKS_ACTION_ATTACK: int = round(TICK_RATE * 1.5)

class ActionAttack(Action):
    def __init__(self, battle: Battle, fighter: Fighter, target: Fighter) -> None:
        Action.__init__(self, TICKS_ACTION_ATTACK)
        self.battle: Battle = battle
        self.fighter: Fighter = fighter
        self.target: Fighter = target

    def isPossible(self) -> bool:
        return self.fighter.canDoActions() and not self.target.isKO()

    def tick(self) -> None:
        if self.ticks <= 0:
            if self.isPossible():
                calc = CalcAttackDamage(self.fighter, self.target)
                self.battle.addEffect(EffectDamage(self.target, calc.damage))
            else:
                # XXX: EffectMiss is used as a catch-all here.
                # XXX: It might be nice to make more distinctions for failure cases.
                # XXX: It might make sense to omit an effect if the target is dead.
                self.battle.addEffect(EffectMiss(self.fighter, self.target))
            self.fighter.actionGauge.reset()
