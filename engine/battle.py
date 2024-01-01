import pygame

import random

import engine

import model

# XXX: Temp stuff.
names = dict()
def getNameOf(thing) -> str:
    result = names.get(thing)
    if result is None:
        result = str(thing)
    return result
def setNameOf(thing, name: str) -> None:
    names[thing] = name
def showMessage(message: str):
    width = 20
    height = 3
    x = random.randint(0, engine.GRID_COLS - 1 - width)
    y = random.randint(0, engine.GRID_ROWS - 1 - height)
    engine.add(engine.DialogQuick(pygame.Rect(x, y, width, height), message))

class Battle(engine.Entity, model.Observer):
    def __init__(self, battle: model.Battle) -> None:
        engine.Entity.__init__(self, mode = engine.Entity.MODE_TICK)
        model.Observer.__init__(self)
        self.battle: model.Battle = battle

        self.battle.addObserver(self)

        # XXX: A hack.
        for fighter in self.battle._fighters:
            if fighter.faction == model.FACTION_PLAYER:
                setNameOf(fighter, 'Maximu')
            else:
                setNameOf(fighter, 'Batson')

    def tick(self) -> None:
        self.battle.tick()

    def cleanup(self) -> None:
        self.battle.removeObserver(self)

    def onTock(self) -> None:
        #showMessage('TOCK')
        pass

    def onActiveAction(self, action: model.Action) -> None:
        text = None
        if action is None:
            text = 'None'
        elif isinstance(action, model.ActionAttack):
            text = getNameOf(action.fighter) + ' is attacking ' + getNameOf(action.target)
        elif isinstance(action, model.ActionMove):
            text = getNameOf(action.fighter) + ' is moving to ' + str(action.coord)
        if text is None:
            text = type(action).__name__ + ' ' + str(action)
        showMessage('ACTION: ' + text)

    def onEffectApplied(self, effect: model.Effect) -> None:
        text = None
        if isinstance(effect, model.EffectAttack):
            text = getNameOf(effect.fighter) + ' deals ' + str(effect.attack.damage) + ' damage to ' + getNameOf(effect.target)
        elif isinstance(effect, model.EffectMove):
            text = getNameOf(effect.fighter) + ' moves to ' + str(effect.coord)
        if text is None:
            text = type(effect).__name__ + ' ' + str(effect)
        showMessage('-> ' + text)

    def onPlayerFighterReady(self, fighter: model.Fighter) -> None:
        showMessage('READY: ' + getNameOf(fighter))
        if random.randint(0, 1) == 0:
            batson = [f for f in self.battle._fighters if f.faction != fighter.faction][0] # XXX TODO
            self.battle.addAction(model.ActionAttack(fighter, batson))
        else:
            x = random.randint(0, model.ZONE_COLS - 1)
            y = random.randint(0, model.ZONE_ROWS - 1)
            self.battle.addAction(model.ActionMove(fighter, (x, y)))

    def onStatusAdd(self, fighter: model.Fighter, status: model.Status) -> None:
        pass

    def onStatusRemove(self, fighter: model.Fighter, status: model.Status) -> None:
        pass

"""
                        # XXX: Doing a basic attack. This should probably live elsewhere. There are other places I look for fighters like this.
                        players = [f for f in self._fighters if f.faction != fighter.faction]
                        if players:
                            self.addAction(model.ActionAttack(fighter, players[0]))
"""

