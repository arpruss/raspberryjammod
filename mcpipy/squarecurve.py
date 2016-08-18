#
# Code by Alexander Pruss and under the MIT license
#

import lsystem
from mineturtle import *
t = Turtle()
t.pendelay(0)
t.turtle(None)
t.penblock(block.BRICK_BLOCK)
t.gridalign()

# http://mathforum.org/advanced/robertd/lsys2d.html
rules = { 'X': 'XF-F+F-XF+F+XF-F+F-X' }

def go():
    t.startface()
    for i in range(4):
        t.go(4)
        t.pitch(90)
    t.endface()
    t.go(4)

dictionary = {
  'F': go,
  '+': lambda: t.yaw(90),
  '-': lambda: t.yaw(-90),
  }

lsystem.lsystem('X', rules, dictionary, 4)
