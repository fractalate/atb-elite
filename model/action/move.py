import model.battle
import model.effect

class Move(model.battle.Action):
    TOTAL_TICKS = model.battle.TICK_RATE // 3 * 2

    def __init__(self, fighter: model.battle.Fighter, coord: tuple[int, int]) -> None:
        model.battle.Action.__init__(self, Move.TOTAL_TICKS)
        self.fighter: model.battle.Fighter = fighter
        self.coord: tuple[int, int] = coord
        self.ticksDue: int = Move.TOTAL_TICKS

    def tick(self, battle: 'model.battle.Battle') -> None:
        if self.ticks >= self.ticksLimit:
            # TODO: determine the hit to the action gauge.
            battle.addEffect(model.effect.Move(self.fighter, self.coord))
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)
