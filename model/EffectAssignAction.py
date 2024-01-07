from model import Action, Battle, Effect, Fighter, Status

class EffectAssignAction(Effect):
    def __init__(self, battle: Battle, fighter: Fighter, action: Action) -> None:
        Effect.__init__(self)
        self.battle: Battle = battle
        self.fighter: Fighter = fighter
        self.action: Status = action

    def apply(self) -> None:
        # Sanity check. Do not handle this error.
        if self.fighter.action is not None:
            raise AssertionError('Fighter already has an action.')
        self.fighter.action = self.action
        if self.action not in self.battle.actionQueue:
            self.battle.actionQueue.append(self.action)
