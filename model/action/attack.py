import model

class ActionAttack(model.Action):
    PRE_STRIKE_TICKS = model.TICK_RATE // 2
    POST_STRIKE_TICKS = model.TICK_RATE // 4
    TOTAL_TICKS = PRE_STRIKE_TICKS + POST_STRIKE_TICKS

    def __init__(self, fighter: model.Fighter, target: model.Fighter) -> None:
        model.Action.__init__(self, ActionAttack.TOTAL_TICKS)
        self.fighter: model.Fighter = fighter
        self.target: model.Fighter = target
        self.ticksDue: int = ActionAttack.PRE_STRIKE_TICKS

    def tick(self, battle: model.Battle) -> None:
        # Early bail out checks come first. If they are expensive, make sure to
        # leverage self.ticksDue to skip calling tick() when it is not needed.
        if model.isKO(self.fighter):
            self.ticksLimit = self.ticks
        # Then, in decreasing order, each tick range at which effects are performed.
        elif self.ticks >= self.ticksLimit:
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)
        elif self.ticks > ActionAttack.PRE_STRIKE_TICKS:
            pass
        elif self.ticks == ActionAttack.PRE_STRIKE_TICKS:
            target = self.target
            if model.isKO(self.target):
                # XXX: Don't use the private data battle._fighters!!!
                targets = [f for f in battle._fighters if f.faction == self.target.faction]
                if targets:
                    target = targets[0]
                    self.target = targets[0]
                else:
                    target = None
            if target is not None:
                battle.addEffect(model.EffectAttack(self.fighter, target))
            self.ticksDue = self.ticksLimit

