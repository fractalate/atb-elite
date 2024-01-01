import engine

import model

def createSampleBattle() -> model.Battle:
    battle = model.Battle()

    fighter = model.Fighter()
    fighter.name = 'Maximu'
    fighter.zone = model.ZONE_RIGHT
    fighter.zoneX = 1
    fighter.zoneY = 0
    fighter.actionGauge.limit = 100
    fighter.hp = fighter.hp_max = 100
    battle.addFighter(fighter)

    fighter = model.Fighter()
    fighter.name = 'Waxus'
    fighter.zone = model.ZONE_RIGHT
    fighter.zoneX = 1
    fighter.zoneY = 1
    fighter.actionGauge.limit = 175
    fighter.hp = fighter.hp_max = 100
    battle.addFighter(fighter)

    fighter = model.Fighter()
    fighter.name = 'Vanus'
    fighter.zone = model.ZONE_RIGHT
    fighter.zoneX = 1
    fighter.zoneY = 2
    fighter.actionGauge.limit = 200
    fighter.hp = fighter.hp_max = 100
    battle.addFighter(fighter)

    fighter = model.Fighter()
    fighter.name = 'Batson'
    fighter.zone = model.ZONE_LEFT
    fighter.zoneX = 1
    fighter.zoneY = 2
    fighter.actionGauge.limit = 75
    fighter.hp = fighter.hp_max = 100
    fighter.faction = model.FACTION_OTHER
    battle.addFighter(fighter)

    return battle

engine.add(engine.Battle(createSampleBattle()))
engine.run()
