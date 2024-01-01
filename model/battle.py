import model

# There are at least two factions in a battle (player vs others):
FACTION_PLAYER: int = 0 # Almost always compare against this constant.
FACTION_OTHER: int = 1 # Any non-zero value is another, distinct faction.

# There are three zones on the battle field:
ZONE_LEFT: int = 0
ZONE_MID: int = 1
ZONE_RIGHT: int = 2

# Each zone is split into a certain number cells as rows and columns:
ZONE_ROWS: int = 4
ZONE_COLS: int = 3

# The battle model requires 30 ticks per second.
TICK_RATE: int = 30 # XXX: Hard coded to match engine.TICK_RATE

# Only one action occurs at a time during battle. An action is something like
# one of your characters swinging their weapon for an attack.
class Action:
    # Fighter action gauges charge during this action.
    MODE_ACTIVE = 0
    # Fighter action gauges do not charge during this action.
    MODE_PAUSE = 1

    def __init__(self, ticksLimit: int, mode: int = MODE_ACTIVE) -> None:
        self.mode: int = mode
        self.ticks: int = 1
        self.ticksLimit: int = ticksLimit
        self.ticksDue: int = 1
        if ticksLimit < 1:
            raise AssertionError('ticksLimit is ' + str(ticksLimit) + ' but must be positive.')

    def tick(self, battle: 'Battle') -> None:
        pass

class Status:
    def __init__(self, ticksLimit: int) -> None:
        # Value is not a Fighter until the status is added to the battle.
        self.fighter: 'Fighter' = None
        self.ticks: int = 1
        self.ticksLimit: int = ticksLimit
        self.ticksDue: int = 1
        if ticksLimit < 1:
            raise AssertionError('ticksLimit is ' + str(ticksLimit) + ' but must be positive.')

    def tick(self, battle: 'Battle') -> None:
        pass

class Script:
    def __init__(self) -> None:
        pass

    def tick(self, battle: 'Battle') -> None:
        pass

class ActionGauge:
    def __init__(self) -> None:
        self.value: int = 0
        self.limit: int = 0

class Fighter(model.StatsBase):
    def __init__(self) -> None:
        model.StatsBase.__init__(self)

        self.name: str = 'Unnamed'
        self.faction: int = FACTION_PLAYER

        self.zone: int = ZONE_LEFT
        self.zoneX: int = 0
        self.zoneY: int = 0

        # For script controlled fighters (enemies).
        self.script: None | Script = None

        self.statuses: list[Status] = []
        self.actionGauge: ActionGauge = ActionGauge()
        self.action: None | Action = None

class Effect:
    def __init__(self) -> None:
        pass

    def apply(self, battle: 'Battle') -> None:
        pass

class Cell:
    NORMAL = 0
    IMPASSIBLE = 1

    def __init__(self) -> None:
        self.state: int = Cell.NORMAL

class Field:
    def __init__(self) -> None:
        self._cells: list[list[list[Cell]]] = [
            [
                [[Cell()
                    for _ in range(ZONE_ROWS)]]
                        for _ in range(ZONE_COLS)
            ] for _ in [
                ZONE_LEFT,
                ZONE_MID,
                ZONE_RIGHT,
            ]
        ]

    def getCell(self, zone: int, col: int, row: int) -> Cell:
        return self._cells[zone][col][row]

class Observer:
    def __init__(self):
        pass

    def onTock(self) -> None:
        pass

    def onActiveAction(self, action: Action) -> None:
        pass

    def onPlayerFighterReady(self, fighter: Fighter) -> None:
        pass

    def onEffectApplied(self, effect: Effect) -> None:
        pass

    def onStatusAdd(self, fighter: Fighter, status: Status) -> None:
        pass

    def onStatusRemove(self, fighter: Fighter, status: Status) -> None:
        pass

class Battle:
    def __init__(self) -> None:
        self._ticks: int = 0
        self._fighters: list[Fighter] = []
        self._field: Field = Field()
        self._playerFighterReadyQueue: list[Field] = []
        self._actionQueue: list[Action] = []
        self._effects: list[Effect] = []
        self._observers: list[Observer] = []
        self._lastAction: None | Action = None

    def addObserver(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def removeObserver(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def addFighter(self, fighter: Fighter) -> None:
        self._fighters.append(fighter)

    def getEnemies(self) -> list[Fighter]:
        return [f for f in self._fighters if f.faction != FACTION_PLAYER]

    def getPlayers(self) -> list[Fighter]:
        return [f for f in self._fighters if f.faction == FACTION_PLAYER]
    
    def getPlayerReady(self) -> None | Fighter:
        if self._playerFighterReadyQueue:
            return self._playerFighterReadyQueue[0]
        return None

    def tick(self) -> None:
        pauseGauges = False

        # Only one action occurs at a time during battle. Each action takes at
        # least 1 tick to complete, so only one action can happen during a tick.
        if self._actionQueue:
            currentAction = self._actionQueue[0]
            pauseGauges = currentAction.mode == Action.MODE_PAUSE
            if currentAction.ticks >= currentAction.ticksLimit or currentAction.ticks >= currentAction.ticksDue:
                currentAction.tick(self) # Called each tick if ticksDue is not set in the action.
            if currentAction.ticks < currentAction.ticksLimit:
                currentAction.ticks += 1
            else:
                self._actionQueue = self._actionQueue[1:]
                self._notifyActionQueue()

        if not pauseGauges:
            if self._ticks < TICK_RATE:
                self._ticks += 1
            else:
                for observer in self._observers:
                    observer.onTock()
                self._ticks = 0

        if not pauseGauges:
            for fighter in self._fighters:
                if isKO(fighter):
                    continue

                if fighter.statuses:
                    for status in list(fighter.statuses):
                        if status.ticks >= status.ticksLimit or status.ticks >= status.ticksDue:
                            status.tick(self)
                        if status.ticks < status.ticksLimit:
                            status.ticks += 1
                        else:
                            fighter.statuses.remove(status)
                            self._notifyStatusRemove(fighter, status)

                # Each fighter's action gauge fills up a little bit on each tick.
                if fighter.actionGauge.value < fighter.actionGauge.limit:
                    fighter.actionGauge.value += 1
                # When a player action bar is full, the fighter is added to a list
                # of ready player fighters. The player can selection actions for
                # these fighters.
                elif fighter.faction == FACTION_PLAYER:
                    if fighter not in self._playerFighterReadyQueue:
                        self._addPlayerFighterReady(fighter)
                # When an enemy's gauge is filled, its script can decide which
                # actions to perform.
                else: 
                    if isinstance(fighter.script, Script):
                        fighter.script.tick(self)

        # All effects, and those created as a result of other effects, are
        # applied this tick.
        while self._effects:
            effect, self._effects = self._effects[0], self._effects[1:]
            self._applyEffect(effect)

    def _addPlayerFighterReady(self, fighter: Fighter) -> None:
        self._playerFighterReadyQueue.append(fighter)
        for observer in self._observers:
            observer.onPlayerFighterReady(fighter)

    def _removePlayerFighterReady(self, fighter: Fighter) -> None:
        if fighter in self._playerFighterReadyQueue:
            self._playerFighterReadyQueue.remove(fighter)

    # Call this whenever you change self._actionQueue.
    def _notifyActionQueue(self) -> None:
        send = False
        if self._actionQueue:
            if self._lastAction is None or self._lastAction is not self._actionQueue[0]:
                self._lastAction = self._actionQueue[0]
                send = True
        elif self._lastAction is not None:
            self._lastAction = None
            send = True
        if send:
            for observer in self._observers:
                observer.onActiveAction(self._lastAction)

    def addAction(self, action: Action) -> None:
        self._actionQueue.append(action)
        self._notifyActionQueue()

    def _notifyStatusRemove(self, fighter: Fighter, status: Status) -> None:
        for observer in self._observers:
            observer.onStatusRemove(fighter, status)

    def addEffect(self, effect: Effect) -> None:
        self._effects.append(effect)

    def addStatus(self, fighter: Fighter, status: Status) -> None:
        if status not in fighter.statuses:
            fighter.statuses.append(status)
            for observer in self._observers:
                observer.onStatusAdd(fighter, status)

    def _applyEffect(self, effect: Effect) -> None:
        effect.apply(self)
        for observer in self._observers:
            observer.onEffectApplied(effect)

def isKO(fighter: Fighter) -> bool:
    return fighter.hp <= 0
