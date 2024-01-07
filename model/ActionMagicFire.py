from model import Action, Battle, CalcMagicFireDamage, Fighter, Status
from model import EffectAssignAction, EffectAssignChargeStatus, EffectDamage, EffectMiss
from model import TICK_RATE

ACTION_MAGIC_FIRE_CHARGE_TICKS = round(TICK_RATE * 2.0)
ACTION_MAGIC_FIRE_CAST_TICKS = round(TICK_RATE * 1.0)

class ActionMagicFireCast(Action):
    def __init__(self, action: 'ActionMagicFire') -> None:
        Action.__init__(self, ACTION_MAGIC_FIRE_CAST_TICKS)
        self.action: ActionMagicFire = action

    def isPossible(self) -> bool:
        return self.action.isPossible()

    def tick(self) -> None:
        if self.ticks <= 0:
            if self.isPossible():
                calc = CalcMagicFireDamage(self.action.fighter, self.action.target)
                self.action.battle.addEffect(EffectDamage(self.action.target, calc.damage))
            else:
                # XXX: EffectMiss is used as a catch-all here.
                # XXX: It might be nice to make more distinctions for failure cases.
                # XXX: It might make sense to omit an effect if the target is dead.
                self.action.battle.addEffect(EffectMiss(self.action.fighter, self.action.target))
            self.action.fighter.actionGauge.reset()

class StatusMagicFireCharge(Status):
    def __init__(self, action: 'ActionMagicFire') -> None:
        Status.__init__(self, action.battle, ACTION_MAGIC_FIRE_CHARGE_TICKS)
        self.action: ActionMagicFire = action

    def tick(self) -> None:
        if self.ticks <= 0:
            nextAction = ActionMagicFire(self.action.battle, self.action.fighter, self.action.target)
            self.battle.addEffect(EffectAssignAction(self.action.battle, self.action.fighter, nextAction))

class ActionMagicFire(Action):
    def __init__(self, battle: Battle, fighter: Fighter, target: Fighter) -> None:
        Action.__init__(self, 1)
        self.battle: Battle = battle
        self.fighter: Fighter = fighter
        self.target: Fighter = target

    def isPossible(self) -> bool:
        return self.fighter.canDoActions() and not self.target.isKO()

    def tick(self) -> None:
        if self.ticks <= 0:
            self.battle.addEffect(EffectAssignChargeStatus(self.battle, self.fighter, StatusMagicFireCharge(self)))

