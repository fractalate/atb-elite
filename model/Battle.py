from model import Action, Effect, Fighter, Status
from model import FACTION_PLAYER
import random

class Battle:
    def __init__(self) -> None:
        self.fighters: list[Fighter] = []
        self.actionQueue: list[Action] = []
        self.effectQueue: list[Effect] = []
        # The game reads this list to see what has happened during the tick.
        self.effects: list[Effect] = []

    def tick(self) -> None:
        pauseFight = False

        # Only one action occurs at a time during battle. Each action takes at
        # least 1 tick to complete, so only one action can happen during a tick.
        if self.actionQueue:
            currentAction = self.actionQueue[0]
            pauseFight = currentAction.mode == Action.MODE_PAUSE
            currentAction.ticks -= 1
            if currentAction.isTickDue():
                currentAction.tick()
            if currentAction.isExpired():
                self.actionQueue = self.actionQueue[1:]

        if not pauseFight:
            for fighter in self.fighters:
                if fighter.isKO():
                    continue

                stopFighter = False
                confuseFighter = False

                if fighter.statuses:
                    for status in list(fighter.statuses):
                        if Status.isStatusStop(status):
                            stopFighter = True
                        if Status.isStatusConfuse(status):
                            confuseFighter = True
                        status.ticks -= 1
                        if status.isTickDue():
                            status.tick()
                        if status.isExpired():
                            fighter.statuses.remove(status)

                if stopFighter:
                    pass
                elif not fighter.actionGauge.isFull():
                    fighter.actionGauge.increment()
                elif fighter.chargeStatus is not None:
                    pass
                elif fighter.action is not None:
                    pass
                elif confuseFighter:
                    self.tickConfuseFighter(fighter)
                elif fighter.script is not None:
                    fighter.script.tick()
                elif fighter.faction != FACTION_PLAYER:
                    self.tickDefaultAction(fighter)

                if fighter.action is not None:
                    if fighter.action.isExpired():
                        fighter.action = None

                if fighter.chargeStatus is not None:
                    if fighter.chargeStatus.isExpired():
                        fighter.chargeStatus = None

        self.effects.clear()
        while self.effectQueue:
            effect, self.effectQueue = self.effectQueue[0], self.effectQueue[1:]
            self.applyEffect(effect)

    def getOpponents(self, faction: int) -> list[Fighter]:
        return [f for f in self.fighters if f.faction != faction]

    def tickConfuseFighter(self, fighter: Fighter) -> None:
        from model import ActionAttack, EffectAssignAction # XXX: Avoiding circular imports.
        target = random.choice(self.fighters)
        action = ActionAttack(self, fighter, target)
        self.addEffect(EffectAssignAction(self, fighter, action))

    def tickDefaultAction(self, fighter: Fighter) -> None:
        from model import ActionAttack, EffectAssignAction # XXX: Avoiding circular imports.
        opponents = self.getOpponents(fighter.faction)
        if opponents:
            target = random.choice(opponents)
            action = ActionAttack(self, fighter, target)
            self.addEffect(EffectAssignAction(self, fighter, action))

    def getCurrentAction(self) -> None | Action:
        if self.actionQueue:
            return self.actionQueue[0]
        return None

    # You should use addEffect() almost surely. Use this for player input actions and battle setup.
    def applyEffect(self, effect: Effect) -> None:
        effect.apply()
        self.effects.append(effect)

    def addEffect(self, effect: Effect) -> None:
        self.effectQueue.append(effect)
