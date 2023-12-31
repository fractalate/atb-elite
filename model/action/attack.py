import model.battle
import model.effect

class Attack(model.battle.Action):
    PRE_STRIKE_TICKS = model.battle.TICK_RATE // 2
    POST_STRIKE_TICKS = model.battle.TICK_RATE // 4
    TOTAL_TICKS = PRE_STRIKE_TICKS + POST_STRIKE_TICKS

    def __init__(self, fighter: model.battle.Fighter, target: model.battle.Fighter) -> None:
        model.battle.Action.__init__(self, Attack.TOTAL_TICKS)
        self.fighter: model.battle.Fighter = fighter
        self.target: model.battle.Fighter = target
        self.ticksDue: int = Attack.PRE_STRIKE_TICKS

    def tick(self, battle: model.battle.Battle) -> None:
        # Early bail out checks come first. If they are expensive, make sure to
        # leverage self.ticksDue to skip calling tick() when it is not needed.
        if model.battle.isKO(self.fighter):
            self.ticksLimit = self.ticks
        # Then, in decreasing order, each tick range at which effects are performed.
        elif self.ticks >= self.ticksLimit:
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)
        elif self.ticks > Attack.PRE_STRIKE_TICKS:
            pass
        elif self.ticks == Attack.PRE_STRIKE_TICKS:
            target = self.target
            if model.battle.isKO(self.target):
                # XXX: Don't use the private data battle._fighters!!!
                targets = [f for f in battle._fighters if f.faction == self.target.faction]
                if targets:
                    target = targets[0]
                    self.target = targets[0]
                else:
                    target = None
            if target is not None:
                battle.addEffect(model.effect.Attack(self.fighter, target))
            self.ticksDue = self.ticksLimit

