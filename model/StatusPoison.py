from model import Battle, CalcPoisonDamage, EffectDamage, Fighter, Status
from model import TICK_RATE

TICKS_STATUS_POISON_DAMAGE = TICK_RATE * 5
TICKS_STATUS_POISON = TICKS_STATUS_POISON_DAMAGE + 4 * TICKS_STATUS_POISON_DAMAGE

class StatusPoison(Status):
    def __init__(self, battle: Battle, fighter: Fighter) -> None:
        Status.__init__(self, battle, TICKS_STATUS_POISON, due = TICKS_STATUS_POISON - TICKS_STATUS_POISON_DAMAGE)
        self.fighter: Fighter = fighter

    def tick(self) -> None:
        if self.ticks <= self.due:
            calc = CalcPoisonDamage()
            self.battle.addEffect(EffectDamage(self.fighter, calc.damage))
            self.due -= TICKS_STATUS_POISON_DAMAGE

