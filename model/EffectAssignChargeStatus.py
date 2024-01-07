from model import Battle, Effect, Fighter, Status

class EffectAssignChargeStatus(Effect):
    def __init__(self, battle: Battle, fighter: Fighter, chargeStatus: Status) -> None:
        Effect.__init__(self)
        self.battle: Battle = battle
        self.fighter: Fighter = fighter
        self.chargeStatus: Status = chargeStatus

    def apply(self) -> None:
        if self.fighter.chargeStatus is not None:
            raise AssertionError('Charge status already assigned.')
        if self.chargeStatus not in self.fighter.statuses:
            self.fighter.statuses.append(self.chargeStatus)
        self.fighter.chargeStatus = self.chargeStatus
