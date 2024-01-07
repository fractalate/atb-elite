from model import Action, FighterActionGauge, Script, StatsBase, Status
from model import FACTION_PLAYER, ZONE_LEFT

class Fighter(StatsBase):
    def __init__(self) -> None:
        StatsBase.__init__(self)
        self.name: str = 'Unnamed'
        self.faction: int = FACTION_PLAYER
        self.zone: int = ZONE_LEFT
        self.coord: tuple[int, int] = 0
        self.action: None | Action = []
        self.statuses: list[Status] = []
        self.chargeStatus: None | Status = []
        self.actionGauge: FighterActionGauge = FighterActionGauge()
        self.script: None | Script = None

    def isKO(self) -> bool:
        return False

    def canDoActions(self) -> bool:
        return self.actionGauge.isFull()
