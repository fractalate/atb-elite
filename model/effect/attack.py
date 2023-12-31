import model

class EffectAttack(model.Effect):
    def __init__(self, fighter: model.Fighter, target: model.Fighter) -> None:
        model.Effect.__init__(self)
        self.fighter: model.Fighter = fighter
        self.target: model.Fighter = target
        self.attack: model.CalcAttack = model.CalcAttack(fighter, target)

    def apply(self, battle: model.Battle) -> None:
        if self.attack.damage > 0:
            # XXX: I likely will need to abstract this logic.
            if self.target.hp <= self.attack.damage:
                self.target.hp = 0
            else:
                self.target.hp -= self.attack.damage
                if self.target.hp > self.target.hp_max:
                    self.target.hp = self.target.hp_max
            if self.target.hp <= 0:
                battle.addEffect(model.EffectKO(self.target))

