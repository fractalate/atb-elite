import pygame
from model import Battle, Fighter
from model import EffectAddFighter, EffectAssignAction
from model import FACTION_OTHER, TICK_RATE, ZONE_LEFT, ZONE_RIGHT

def createSampleBattle() -> Battle:
    battle = Battle()

    fighter = Fighter()
    fighter.name = 'Maximu'
    fighter.zone = ZONE_RIGHT
    fighter.coord = (1, 0)
    fighter.actionGauge.limit = 100
    fighter.hp = fighter.hp_max = 100
    battle.applyEffect(EffectAddFighter(battle, fighter))

    fighter = Fighter()
    fighter.name = 'Batson A'
    fighter.zone = ZONE_LEFT
    fighter.coord = (0, 0)
    fighter.actionGauge.limit = 75
    fighter.hp = fighter.hp_max = 100
    fighter.faction = FACTION_OTHER
    battle.applyEffect(EffectAddFighter(battle, fighter))

    return battle

def narrateBattle(battle: Battle):
    if battle.effects:
        print()
        for effect in battle.effects:
            print(type(effect), effect)

clock = pygame.time.Clock()
battle = createSampleBattle()
narrateBattle(battle)
clock.tick(TICK_RATE)
while True:
    battle.tick()
    narrateBattle(battle)
    clock.tick(TICK_RATE)
