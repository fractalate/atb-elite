import time

import model.battle

names = dict()
def getNameOf(thing) -> str:
    result = names.get(thing)
    if result is None:
        result = str(thing)
    return result
def setNameOf(thing, name: str) -> None:
    names[thing] = name

class Observer(model.battle.ModelBattleObserver):
    def __init__(self):
        model.battle.ModelBattleObserver.__init__(self)

    def onTock(self) -> None:
        print('TOCK')

    def onActiveAction(self, action: model.battle.ModelBattleAction) -> None:
        text = None
        if action is None:
            text = 'None'
        elif isinstance(action, model.battle.ModelBattleActionAttack):
            text = getNameOf(action.fighter) + ' is attacking ' + getNameOf(action.target)
        if text is None:
            text = type(action).__name__ + ' ' + str(action)
        print('ACTION:', text)

    def onEffectApplied(self, effect: model.battle.ModelBattleEffect) -> None:
        text = None
        if isinstance(effect, model.battle.ModelBattleEffectAttack):
            text = getNameOf(effect.fighter) + ' deals ' + str(effect.attack.damage) + ' damage to ' + getNameOf(effect.target)
        if text is None:
            text = type(effect).__name__ + ' ' + str(effect)
        print('  ->', text)

    def onPlayerFighterReady(self, fighter: model.battle.ModelBattleFighter) -> None:
        print('READY:', getNameOf(fighter))


battle = model.battle.ModelBattle()
battle.addObserver(Observer())

fighter = model.battle.ModelBattleFighter()
fighter.actionGauge.limit = 100
fighter.hp = fighter.hp_max = 100
battle.addFighter(fighter)
setNameOf(fighter, 'Maximu')

fighter = model.battle.ModelBattleFighter()
fighter.actionGauge.limit = 75
fighter.hp = fighter.hp_max = 100
fighter.faction = model.battle.FACTION_OTHER
battle.addFighter(fighter)
setNameOf(fighter, 'Batson')

while True:
    battle.tick()
    time.sleep(1 / 30)
