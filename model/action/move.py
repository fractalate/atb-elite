import model

class ActionMove(model.Action):
    TOTAL_TICKS = model.TICK_RATE // 3 * 2

    def __init__(self, fighter: model.Fighter, coord: tuple[int, int]) -> None:
        model.Action.__init__(self, ActionMove.TOTAL_TICKS)
        self.fighter: model.Fighter = fighter
        self.coord: tuple[int, int] = coord
        self.ticksDue: int = ActionMove.TOTAL_TICKS

    def tick(self, battle: model.Battle) -> None:
        if self.ticks >= self.ticksLimit:
            # TODO: determine the hit to the action gauge.
            battle.addEffect(model.EffectMove(self.fighter, self.coord))
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)
