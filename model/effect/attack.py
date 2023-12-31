import model.battle
import model.calc
import model.effect

class Attack(model.battle.Effect):
    def __init__(self, fighter: model.battle.Fighter, target: model.battle.Fighter) -> None:
        model.battle.Effect.__init__(self)
        self.fighter: model.battle.Fighter = fighter
        self.target: model.battle.Fighter = target
        self.attack: model.calc.CalcAttack = model.calc.CalcAttack(fighter, target)

    def apply(self, battle: model.battle.Battle) -> None:
        if self.attack.damage > 0:
            # XXX: I likely will need to abstract this logic.
            if self.target.hp <= self.attack.damage:
                self.target.hp = 0
            else:
                self.target.hp -= self.attack.damage
                if self.target.hp > self.target.hp_max:
                    self.target.hp = self.target.hp_max
            if self.target.hp <= 0:
                battle.addEffect(model.effect.KO(self.target))

