import model.calc
import model.stats


################################################################################
### CONSTANTS                                                                ###
################################################################################

# There are at least two factions in a battle (player vs others):
FACTION_PLAYER = 0 # Almost always compare against this constant.
FACTION_OTHER = 1 # Any non-zero value is another, distinct faction.

# There are three zones on the battlefield:
ZONE_LEFT = 0
ZONE_MID = 1
ZONE_RIGHT = 2

# Each zone is split into a certain number cells as rows and columns:
ZONE_ROWS = 4
ZONE_COLS = 3

# Cells on the battlefield can be in various states:
CELL_NORMAL = 0
CELL_IMPASSIBLE = 1

# The battle model requires 30 ticks per second.
TICK_RATE = 30

# Some actions can pause ticks delivered to fighters. See ModeBattleAction.
ACT_MODE_ACTIVE = 0
ACT_MODE_PAUSE = 1


################################################################################
### BATTLE ENTITIES                                                          ###
################################################################################

class ModelBattleFighterActionGauge:
    def __init__(self) -> None:
        self.value: int = 0
        self.limit: int = 0

class ModelBattleFighter(model.stats.ModelStatsBase):
    def __init__(self) -> None:
        model.stats.ModelStatsBase.__init__(self)

        self.faction: int = FACTION_PLAYER

        self.zone: int = ZONE_LEFT
        self.zoneX: int = 0
        self.zoneY: int = 0

        # For script controlled fighters (enemies).
        self.script: None | ModelBattleScript = None

        self.actionGauge: ModelBattleFighterActionGauge = ModelBattleFighterActionGauge()
        self.action: None | ModelBattleAction = None


################################################################################
### BATTLE EFFECTS                                                           ###
################################################################################

class ModelBattleEffect:
    def __init__(self) -> None:
        pass

    def apply(self, battle: 'ModelBattle') -> None:
        pass

class ModelBattleEffectFighterKO(ModelBattleEffect):
    def __init__(self, fighter: ModelBattleFighter) -> None:
        ModelBattleEffect.__init__(self)
        self.fighter: ModelBattleFighter = fighter

class ModelBattleEffectAttack(ModelBattleEffect):
    def __init__(self, fighter: ModelBattleFighter, target: ModelBattleFighter) -> None:
        ModelBattleEffect.__init__(self)
        self.fighter: ModelBattleFighter = fighter
        self.target: ModelBattleFighter = target
        self.attack: model.calc.CalcAttack = model.calc.CalcAttack(fighter, target)

    def apply(self, battle: 'ModelBattle') -> None:
        if self.attack.damage > 0:
            # XXX: I likely will need to abstract this logic.
            if self.target.hp <= self.attack.damage:
                self.target.hp = 0
            else:
                self.target.hp -= self.attack.damage
                if self.target.hp > self.target.hp_max:
                    self.target.hp = self.target.hp_max
            if self.target.hp <= 0:
                battle.addEffect(ModelBattleEffectFighterKO(self.target))

class ModelBattleEffectFighterMove(ModelBattleEffect):
    def __init__(self, fighter: ModelBattleFighter, coord: tuple[int, int]) -> None:
        ModelBattleEffect.__init__(self)
        self.fighter: ModelBattleFighter = fighter
        self.coord: tuple[int, int] = coord

    def apply(self, battle: 'ModelBattle') -> None:
        self.fighter.zoneX, self.fighter.zoneY = self.coord

################################################################################
### BATTLE ACTIONS                                                           ###
################################################################################

def isKO(fighter: ModelBattleFighter) -> bool:
    return fighter.hp <= 0

class ModelBattleAction:
    def __init__(self, ticksLimit: int, mode: int = ACT_MODE_ACTIVE) -> None:
        self.mode: int = mode
        self.ticks: int = 1
        self.ticksLimit: int = ticksLimit
        self.ticksDue: int = 1
        if ticksLimit < 1:
            raise AssertionError('ticksLimit is ' + str(ticksLimit) + ' but must be positive.')

    def tick(self, battle: 'ModelBattle') -> None:
        pass

class ModelBattleActionAttack(ModelBattleAction):
    PRE_STRIKE_TICKS = TICK_RATE // 2
    POST_STRIKE_TICKS = TICK_RATE // 4
    TOTAL_TICKS = PRE_STRIKE_TICKS + POST_STRIKE_TICKS

    def __init__(self, fighter: ModelBattleFighter, target: ModelBattleFighter) -> None:
        ModelBattleAction.__init__(self, ModelBattleActionAttack.TOTAL_TICKS)
        self.fighter: ModelBattleFighter = fighter
        self.target: ModelBattleFighter = target
        self.ticksDue: int = ModelBattleActionAttack.PRE_STRIKE_TICKS

    def tick(self, battle: 'ModelBattle') -> None:
        # Early bail out checks come first. If they are expensive, make sure to
        # leverage self.ticksDue to skip calling tick() when it is not needed.
        if isKO(self.fighter):
            self.ticksLimit = self.ticks
        # Then, in decreasing order, each tick range at which effects are performed.
        elif self.ticks >= self.ticksLimit:
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)
        elif self.ticks > ModelBattleActionAttack.PRE_STRIKE_TICKS:
            pass
        elif self.ticks == ModelBattleActionAttack.PRE_STRIKE_TICKS:
            target = self.target
            if isKO(self.target):
                # XXX: Don't use the private data battle._fighters!!!
                targets = [f for f in battle._fighters if f.faction == self.target.faction]
                if targets:
                    target = targets[0]
                    self.target = targets[0]
                else:
                    target = None
            if target is not None:
                battle.addEffect(ModelBattleEffectAttack(self.fighter, target))
            self.ticksDue = self.ticksLimit


class ModelBattleActionMove(ModelBattleAction):
    TOTAL_TICKS = TICK_RATE // 3 * 2

    def __init__(self, fighter: ModelBattleFighter, coord: tuple[int, int]) -> None:
        ModelBattleAction.__init__(self, ModelBattleActionMove.TOTAL_TICKS)
        self.fighter: ModelBattleFighter = fighter
        self.coord: tuple[int, int] = coord
        self.ticksDue: int = ModelBattleActionMove.TOTAL_TICKS

    def tick(self, battle: 'ModelBattle') -> None:
        if self.ticks >= self.ticksLimit:
            # TODO: determine the hit to the action gauge.
            battle.addEffect(ModelBattleEffectFighterMove(self.fighter, self.coord))
            self.fighter.actionGauge.value = 0 # XXX: Action gauge resets could be its own effect? Multiple of these.
            battle._removePlayerFighterReady(self.fighter)


################################################################################
### BATTLE SCRIPTING                                                         ###
################################################################################

class ModelBattleScript:
    def __init__(self) -> None:
        pass

    def tick(self, battle: 'ModelBattle') -> None:
        pass


################################################################################
### BATTLE FIELD                                                             ###
################################################################################

class ModelBattleFieldCell:
    def __init__(self) -> None:
        self.state: int = CELL_NORMAL

class ModelBattleField:
    def __init__(self) -> None:
        self._cells: list[list[list[ModelBattleFieldCell]]] = [
            [
                [[ModelBattleFieldCell()
                    for _ in range(ZONE_ROWS)]]
                        for _ in range(ZONE_COLS)
            ] for _ in [
                ZONE_LEFT,
                ZONE_MID,
                ZONE_RIGHT,
            ]
        ]

    def getCell(self, zone: int, col: int, row: int) -> ModelBattleFieldCell:
        return self._cells[zone][col][row]


################################################################################
### BATTLE OBSERVER                                                          ###
################################################################################

class ModelBattleObserver:
    def __init__(self):
        pass

    def onTock(self) -> None:
        pass

    def onActiveAction(self, action: ModelBattleAction) -> None:
        pass

    def onPlayerFighterReady(self, fighter: ModelBattleFighter) -> None:
        pass

    def onEffectApplied(self, effect: ModelBattleEffect) -> None:
        pass


################################################################################
### BATTLE                                                                   ###
################################################################################

class ModelBattle:
    def __init__(self) -> None:
        self._ticks: int = 0
        self._fighters: list[ModelBattleFighter] = []
        self._field: ModelBattleField = ModelBattleField()
        self._playerFighterReadyQueue: list[ModelBattleField] = []
        self._actionQueue: list[ModelBattleAction] = []
        self._effects: list[ModelBattleEffect] = []
        self._observers: list[ModelBattleObserver] = []
        self._lastAction: None | ModelBattleAction = None

    def addObserver(self, observer: ModelBattleObserver) -> None:
        self._observers.append(observer)

    def addFighter(self, fighter: ModelBattleFighter) -> None:
        self._fighters.append(fighter)

    def tick(self) -> None:
        pauseGauges = False

        # Only one action occurs at a time during battle. Each action takes at
        # least 1 tick to complete, so only one action can happen during a tick.
        if self._actionQueue:
            currentAction = self._actionQueue[0]
            pauseGauges = currentAction.mode == ACT_MODE_PAUSE
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

                # TODO: Tick the fighter. Possibly things like poison damage need to be applied.

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
                    if isinstance(fighter.script, ModelBattleScript):
                        fighter.script.tick(self)
                    else:
                        # XXX: Doing a basic attack. This should probably live elsewhere. There are other places I look for fighters like this.
                        players = [f for f in self._fighters if f.faction != fighter.faction]
                        if players:
                            self.addAction(ModelBattleActionAttack(fighter, players[0]))

        # All effects, and those created as a result of other effects, are
        # applied this tick.
        while self._effects:
            effect, self._effects = self._effects[0], self._effects[1:]
            self._applyEffect(effect)

    def _addPlayerFighterReady(self, fighter: ModelBattleFighter) -> None:
        self._playerFighterReadyQueue.append(fighter)
        for observer in self._observers:
            observer.onPlayerFighterReady(fighter)

    def _removePlayerFighterReady(self, fighter: ModelBattleFighter) -> None:
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

    def addAction(self, action: ModelBattleAction) -> None:
        self._actionQueue.append(action)
        self._notifyActionQueue()

    def addEffect(self, effect: ModelBattleEffect) -> None:
        self._effects.append(effect)

    def _applyEffect(self, effect: ModelBattleEffect) -> None:
        effect.apply(self)
        for observer in self._observers:
            observer.onEffectApplied(effect)
