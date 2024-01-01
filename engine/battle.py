import pygame

import random

import engine

import model

# XXX: Temp stuff.
lines = 0
def showMessage(message: str):
    global lines
    width = 20
    height = 3
    x = 0
    y = lines
    lines += height
    if lines >= engine.GRID_ROWS - height:
        lines = 0
    engine.add(engine.DialogQuick(pygame.Rect(x, y, width, height), message))

class EnemyList(engine.Entity):
    def __init__(self, battle: model.Battle) -> None:
        engine.Entity.__init__(self, engine.Entity.MODE_RENDER)
        self.battle: model.Battle = battle
        self.dialog: engine.Dialog = engine.Dialog(pygame.Rect(0, 20, 18, 4))
        engine.add(self.dialog)
        self.updateText()

    def cleanup(self) -> None:
        engine.remove(self.dialog)

    def updateText(self) -> None:
        names = [e.name for e in self.battle.getEnemies() if not model.isKO(e)]
        self.dialog.setText('\n'.join(names))

class PlayerList(engine.Entity):
    def __init__(self, battle: model.Battle) -> None:
        engine.Entity.__init__(self, engine.Entity.MODE_RENDER)
        self.battle: model.Battle = battle
        self.dialog = engine.Dialog(pygame.Rect(18, 20, 20, 4))
        engine.add(self.dialog)
        self.updateText()

    def cleanup(self):
        engine.remove(self.dialog)

    def updateText(self) -> None:
        names = [e.name for e in self.battle.getPlayers() if not model.isKO(e)]
        self.dialog.setText('\n'.join(names))

class Battle(engine.Entity, model.Observer):
    def __init__(self, battle: model.Battle) -> None:
        engine.Entity.__init__(self, mode = engine.Entity.MODE_TICK)
        model.Observer.__init__(self)
        self.battle: model.Battle = battle
        self.battle.addObserver(self)
        self.enemyList: EnemyList = EnemyList(self.battle)
        engine.add(self.enemyList)
        self.playerList: PlayerList = PlayerList(self.battle)
        engine.add(self.playerList)

    def cleanup(self) -> None:
        self.battle.removeObserver(self)
        engine.remove(self.enemyList)
        engine.remove(self.playerList)

    def tick(self) -> None:
        self.battle.tick()

    def onTock(self) -> None:
        #showMessage('TOCK')
        pass

    def onActiveAction(self, action: model.Action) -> None:
        text = None
        if action is None:
            text = 'None'
        elif isinstance(action, model.ActionAttack):
            text = action.fighter.name + ' is attacking ' + action.target.name
        elif isinstance(action, model.ActionMove):
            text = action.fighter.name + ' is moving to ' + str(action.coord)
        if text is None:
            text = type(action).__name__ + ' ' + str(action)
        showMessage('ACTION: ' + text)

    def onEffectApplied(self, effect: model.Effect) -> None:
        text = None
        if isinstance(effect, model.EffectAttack):
            text = effect.fighter.name + ' deals ' + str(effect.attack.damage) + ' damage to ' + effect.target.name
        elif isinstance(effect, model.EffectMove):
            text = effect.fighter.name + ' moves to ' + str(effect.coord)
        if text is None:
            text = type(effect).__name__ + ' ' + str(effect)
        showMessage('-> ' + text)

    def onPlayerFighterReady(self, fighter: model.Fighter) -> None:
        showMessage('READY: ' + fighter.name)
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

