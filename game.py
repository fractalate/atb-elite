import engine

import model

def createSampleBattle() -> model.Battle:
    battle = model.Battle()

    fighter = model.Fighter()
    fighter.actionGauge.limit = 100
    fighter.hp = fighter.hp_max = 100
    battle.addFighter(fighter)

    fighter = model.Fighter()
    fighter.actionGauge.limit = 75
    fighter.hp = fighter.hp_max = 100
    fighter.faction = model.FACTION_OTHER
    battle.addFighter(fighter)

    return battle

engine.add(engine.Battle(createSampleBattle()))
engine.run()
