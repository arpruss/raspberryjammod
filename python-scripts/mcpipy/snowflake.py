#
# Code under the MIT license by Alexander Pruss
#

import lsystem
from mcturtle import *
t = Turtle()
t.pendelay(0)
t.penblock(GOLD_BLOCK)
t.turtle(None)

rules = { 'F': 'F-F++F-F' }
axiom = 'F++F++F'

dictionary = {
  'F': lambda: t.go(2),
  '+': lambda: t.yaw(60),
  '-': lambda: t.yaw(-60),
  }

lsystem.lsystem(axiom, rules, dictionary, 4)
