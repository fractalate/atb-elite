import pygame

import random
import textwrap

import engine
import engine.dialog
import engine.grid
import engine.text
import model.action
import model.battle
import model.effect
import model.status

Z_SCENE   = 0
Z_PLAYERS = 10
Z_ACTION  = 20
Z_DIALOG  = 30
Z_DEBUG   = 100

names = dict()
def getNameOf(thing) -> str:
    result = names.get(thing)
    if result is None:
        result = str(thing)
    return result
def setNameOf(thing, name: str) -> None:
    names[thing] = name

import random
class MessageEntity(engine.Entity):
    def __init__(self, message: str) -> None:
        engine.Entity.__init__(self, mode = engine.Entity.MODE_RENDER, frames = 20)
        x = random.randint(0, engine.grid.GRID_COLS - 1 - 20)
        y = random.randint(0, engine.grid.GRID_ROWS - 1 - 3)
        width = 20
        height = 3
        self.gcoord = (x, y)
        self.dialog = engine.dialog.Dialog(pygame.Rect(x, y, width, height))
        self.text = engine.text.BasicText((width, height), message)

    def render(self, surface: pygame.Surface) -> None:
        self.dialog.render(surface)
        self.text.render(surface, self.gcoord)

def showMessage(message: str):
    message = '\n'.join(textwrap.wrap(message, width = 20))
    engine.add(MessageEntity(message))

class Observer(model.battle.Observer):
    def __init__(self) -> None:
        model.battle.Observer.__init__(self)

    def onTock(self) -> None:
        showMessage('TOCK')

    def onActiveAction(self, action: model.battle.Action) -> None:
        text = None
        if action is None:
            text = 'None'
        elif isinstance(action, model.action.Attack):
            text = getNameOf(action.fighter) + ' is attacking ' + getNameOf(action.target)
        elif isinstance(action, model.action.Move):
            text = getNameOf(action.fighter) + ' is moving to ' + str(action.coord)
        if text is None:
            text = type(action).__name__ + ' ' + str(action)
        showMessage('ACTION: ' + text)

    def onEffectApplied(self, effect: model.battle.Effect) -> None:
        text = None
        if isinstance(effect, model.effect.Attack):
            text = getNameOf(effect.fighter) + ' deals ' + str(effect.attack.damage) + ' damage to ' + getNameOf(effect.target)
        elif isinstance(effect, model.effect.Move):
            text = getNameOf(effect.fighter) + ' moves to ' + str(effect.coord)
        if text is None:
            text = type(effect).__name__ + ' ' + str(effect)
        showMessage('  -> ' + text)

    def onPlayerFighterReady(self, fighter: model.battle.Fighter) -> None:
        showMessage('READY: ' + getNameOf(fighter))
        if random.randint(0, 1) == 0:
            battle.addAction(model.action.Attack(fighter, batson))
        else:
            x = random.randint(0, model.battle.ZONE_COLS - 1)
            y = random.randint(0, model.battle.ZONE_ROWS - 1)
            battle.addAction(model.action.Move(fighter, (x, y)))

    def onStatusAdd(self, fighter: model.battle.Fighter, status: model.battle.Status) -> None:
        pass

    def onStatusRemove(self, fighter: model.battle.Fighter, status: model.battle.Status) -> None:
        pass

class BattleEntity(engine.Entity):
    def __init__(self):
        engine.Entity.__init__(self, mode = engine.Entity.MODE_TICK)

    def tick(self) -> None:
        battle.tick()

battle = model.battle.Battle()
battle.addObserver(Observer())

maximu = fighter = model.battle.Fighter()
fighter.actionGauge.limit = 100
fighter.hp = fighter.hp_max = 100
battle.addFighter(fighter)
setNameOf(fighter, 'Maximu')

batson = fighter = model.battle.Fighter()
fighter.actionGauge.limit = 75
fighter.hp = fighter.hp_max = 100
fighter.faction = model.battle.FACTION_OTHER
battle.addFighter(fighter)
setNameOf(fighter, 'Batson')

engine.add(BattleEntity())
engine.run()

"""
                        # XXX: Doing a basic attack. This should probably live elsewhere. There are other places I look for fighters like this.
                        players = [f for f in self._fighters if f.faction != fighter.faction]
                        if players:
                            self.addAction(model.action.Attack(fighter, players[0]))
"""
