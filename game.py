# Do this first to bootstrap various things.
import lib.bootstrap

import pygame

import lib.game
import lib.battle

game = lib.game.Game()

# The game should probably start in some generic way, but start it with a battle
# for now since a lot of development will focus on the battle implementation.
battle = lib.battle.Battle()
game.startBattle(battle)

game.run()

pygame.quit()
