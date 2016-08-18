#
# Code by Alexander Pruss and under the MIT license
#

import lsystem
from mineturtle import *

t = Turtle()
t.pendelay(0)
t.penblock(block.WOOD)
t.turtle(None)
t.pitch(90)

rules = {'L':'[^FL]>[^FL]>[^FL]'}
axiom = 'FL'

dictionary = {
  'F': lambda: t.go(10),
  '+': lambda: t.yaw(90),
  '-': lambda: t.yaw(-90),
  '^': lambda: t.pitch(20),
  '&': lambda: t.pitch(-20),
  '>': lambda: t.roll(120),
  '<': lambda: t.roll(-120),
  '[': lambda: t.push(),
  ']': lambda: t.pop()
  }

lsystem.lsystem(axiom,rules,dictionary,5)
