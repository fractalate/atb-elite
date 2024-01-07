from model import Battle, Effect, EffectKO, Fighter

class EffectDamage(Effect):
    def __init__(self, battle: Battle, fighter: Fighter, damage: int) -> None:
        Effect.__init__(self)
        self.battle = battle
        self.fighter = fighter
        self.damage = damage

    def apply(self) -> None:
        if self.damage >= self.fighter.hp:
            self.fighter.hp = 0
            self.battle.addEffect(EffectKO(self.fighter))
        else:
            self.fighter.hp -= self.damage
            if self.fighter.hp > self.fighter.hp_max:
                self.fighter.hp = self.fighter.hp_max
