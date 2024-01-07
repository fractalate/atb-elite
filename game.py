from model import Battle, Fighter
from model import EffectAddFighter, EffectAssignAction
from model import ZONE_LEFT, ZONE_RIGHT, FACTION_OTHER

def createSampleBattle() -> Battle:
    battle = Battle()

    fighter = Fighter()
    fighter.name = 'Maximu'
    fighter.zone = ZONE_RIGHT
    fighter.coord = (1, 0)
    fighter.actionGauge.limit = 100
    fighter.hp = fighter.hp_max = 100
    EffectAddFighter(battle, fighter).apply()

    fighter = Fighter()
    fighter.name = 'Batson A'
    fighter.zone = ZONE_LEFT
    fighter.coord = (0, 0)
    fighter.actionGauge.limit = 75
    fighter.hp = fighter.hp_max = 100
    fighter.faction = FACTION_OTHER
    EffectAddFighter(battle, fighter).apply()

    return battle

battle = Battle()
while True:
    battle.tick()
