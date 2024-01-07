# Which zone?
ZONE_LEFT = 0
ZONE_MID = 1
ZONE_RIGHT = 2

# How big is each zone?
ZONE_COLS = 3
ZONE_ROWS = 4

# Ticks per second.
TICK_RATE = 30

# Player has faction 0. All other numbers indicate other enemy factions.
FACTION_PLAYER = 0
# For convenience/clarity where it is used.
FACTION_OTHER = 1

# Elementary structures to be imported first.
from model.BattleField import BattleField
from model.BattleFieldCell import BattleFieldCell
from model.Clocked import Clocked
from model.FighterActionGauge import FighterActionGauge
from model.Script import Script
from model.StatsDamage import StatsDamage
from model.StatsBase import StatsBase

# Base classes for things which go on during the battle.
# These depend on the imports above.
from model.Action import Action
from model.Effect import Effect
from model.Status import Status

# Main classes. These depend on the imports above.
from model.Battle import Battle
from model.Fighter import Fighter

# Calculations are used by actions and statuses, so they come before both.
# These depend on the imports above.
from model.CalcAttackDamage import CalcAttackDamage
from model.CalcMagicFireDamage import CalcMagicFireDamage
from model.CalcPoisonDamage import CalcPoisonDamage

# Actions. These depend on the imports above.
from model.ActionAttack import ActionAttack
from model.ActionMagicFire import ActionMagicFire
from model.ActionMove import ActionMove

# Effects. These depend on the imports above.
from model.EffectAddFighter import EffectAddFighter
from model.EffectAssignAction import EffectAssignAction
from model.EffectAssignChargeStatus import EffectAssignChargeStatus
from model.EffectDamage import EffectDamage
from model.EffectKO import EffectKO

# Statuses. These depend on the imports above.
from model.StatusPoison import StatusPoison
from model.StatusStop import StatusStop
