# Do this first to bootstrap various things.
import lib.bootstrap

import pygame

import lib.fighter
import lib.game
import lib.battle

game = lib.game.Game()

# The game should probably start in some generic way, but start it with a battle
# for now since a lot of development will focus on the battle implementation.
battle = lib.battle.Battle()

fighterMaximu = lib.fighter.SampleFighter()
fighterMaximu.hp = 1234
fighterAudry = lib.fighter.SampleFighter()
fighterAudry.spd = 0
fighterJack = lib.fighter.SampleFighter()
fighterJack.spd = 255
battle.addFighter(lib.battle.FACTION_PLAYER, lib.battle.ZONE_RIGHT, 'Maximu', fighterMaximu, (1, 0, 1, 1))
battle.addFighter(lib.battle.FACTION_PLAYER, lib.battle.ZONE_RIGHT, 'Audry', fighterAudry, (1, 1, 1, 1))
battle.addFighter(lib.battle.FACTION_PLAYER, lib.battle.ZONE_RIGHT, 'Jack', fighterJack, (1, 2, 1, 1))

fighterBatson = lib.fighter.SampleFighter()
battle.addFighter(lib.battle.FACTION_OTHER, lib.battle.ZONE_LEFT, 'Batson', fighterJack, (1, 3, 1, 1))

game.startBattle(battle)

game.run()

pygame.quit()
