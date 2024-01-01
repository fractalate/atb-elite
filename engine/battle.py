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
        self.dialog: engine.Dialog = engine.Dialog(pygame.Rect(0, 20, 18, 4)) # TODO: Move constants to a common place.
        engine.add(self.dialog)
        self.updateText()

    def cleanup(self) -> None:
        engine.remove(self.dialog)

    def updateText(self) -> None:
        names = [e.name for e in self.battle.getEnemies() if not model.isKO(e)]
        self.dialog.setText('\n'.join(names))

class PlayerListEntry:
    def __init__(self, slot: int, fighter: model.Fighter, battle: model.Battle) -> None:
        self.slot: int = slot
        self.fighter: model.Fighter = fighter
        self.battle: model.Battle = battle
        self.text: engine.PalletteText = None
        self.progressBar: ProgressBar = ProgressBar(self.fighter)
        self.updateText()

    def render(self, surface: pygame.Surface) -> None:
        self.progressBar.render(surface, pygame.Rect(32 - 3, 20 + self.slot, 3, 1))
        if self.battle.getPlayerReady() is self.fighter:
            pallette = engine.PALLETTE_YELLOW
        elif model.isKO(self.fighter):
            pallette = engine.PALLETTE_RED
        else:
            pallette = engine.PALLETTE_WHITE
        self.text.render(surface, (18, 20 + self.slot), pallette = pallette) # TODO: Move constants to a common place.

    def updateText(self) -> None:
        lineText = '{:<6s} {:4d}'.format(self.fighter.name, self.fighter.hp)
        self.text = engine.PalletteText((17, 1), lineText) # TODO: Move constants to a common place.

class ProgressBar:
    def __init__(self, fighter: model.Fighter) -> None:
        self.fighter: model.Fighter = fighter

    def render(self, surface: pygame.Surface, grect: pygame.Rect) -> None:
        x, y = engine.gridCoordToScreen((grect.x, grect.y))
        width, height = engine.gridCoordToScreen((grect.w, grect.h))
        height -= engine.GRID_STEP_Y // 2
        y += engine.GRID_STEP_Y // 4
        pygame.draw.rect(surface, (0x00, 0x00, 0x00), (x, y, width, height)) # TODO: Constant color.
        if self.fighter.actionGauge.value > 0:
            fillPercent = self.fighter.actionGauge.value / self.fighter.actionGauge.limit
            fillWidth = fillPercent * width
            pygame.draw.rect(surface, (0x11, 0xAB, 0x33), (x, y, fillWidth, height)) # TODO: Constant color.

class PlayerList(engine.Entity):
    def __init__(self, battle: model.Battle) -> None:
        engine.Entity.__init__(self, engine.Entity.MODE_RENDER)
        self.battle: model.Battle = battle
        self.dialog = engine.Dialog(pygame.Rect(18, 20, 20, 4)) # TODO: Move constants to a common place.
        self.entries: list[PlayerListEntry] = [PlayerListEntry(slot, f, self.battle) for slot, f in enumerate(self.battle.getPlayers())]
        engine.add(self.dialog)
        self.updateText()

    def cleanup(self) -> None:
        engine.remove(self.dialog)

    def updateText(self) -> None:
        for entry in self.entries:
            entry.updateText()

    def render(self, surface: pygame.Surface) -> None:
        for entry in self.entries:
            entry.render(surface)

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

