#
# Code by Alexander Pruss and under the MIT license
#

import lsystem
from mineturtle import *
from sys import argv
COLORS = (block.WOOL_WHITE,block.HARDENED_CLAY_STAINED_WHITE,block.WOOL_PINK,block.WOOL_MAGENTA,block.WOOL_PURPLE,block.HARDENED_CLAY_STAINED_LIGHT_BLUE,block.HARDENED_CLAY_STAINED_CYAN,block.HARDENED_CLAY_STAINED_PURPLE,block.HARDENED_CLAY_STAINED_LIGHT_GRAY,block.HARDENED_CLAY_STAINED_MAGENTA,block.HARDENED_CLAY_STAINED_PINK,block.HARDENED_CLAY_STAINED_RED,block.WOOL_RED,block.REDSTONE_BLOCK,block.HARDENED_CLAY_STAINED_ORANGE,block.WOOL_ORANGE,block.HARDENED_CLAY_STAINED_YELLOW,block.WOOL_YELLOW,block.WOOL_LIME,block.HARDENED_CLAY_STAINED_LIME,block.HARDENED_CLAY_STAINED_GREEN,block.WOOL_GREEN,block.HARDENED_CLAY_STAINED_GRAY,block.WOOL_BROWN,block.HARDENED_CLAY_STAINED_BROWN,block.WOOL_GRAY,block.HARDENED_CLAY_STAINED_BLUE,block.WOOL_BLUE,block.WOOL_CYAN,block.WOOL_LIGHT_BLUE,block.WOOL_LIGHT_GRAY)
t = Turtle()
t.pendelay(0)
t.turtle(None)
t.penblock(block.STAINED_GLASS_PURPLE)
t.gridalign()

# rules from
# http://kanga.nu/~claw/blog/2008/11/16/game-design-tools/inkscape-l-systems-svg-penrose-and-other-tilings/
rules = { 'W': '+++X--F--ZFX+',
          'X': '---W++F++YFW-',
          'Y': '+ZFX--F--Z+++',
          'Z': '-YFW++F++Y---',
          }
axiom = 'W'

colorIndex = 0
def go():
    global colorIndex
    t.penblock(COLORS[colorIndex % len(COLORS)])
    colorIndex += 1
    t.go(6)

    

dictionary = {
  'F': go,
  '+': lambda: t.yaw(-30),
  '-': lambda: t.yaw(30),
  '[': lambda: t.push(),
  ']': lambda: t.pop()
  }

lsystem.lsystem(axiom, rules, dictionary, 6)
