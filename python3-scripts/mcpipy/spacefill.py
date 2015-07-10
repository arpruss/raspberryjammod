#
# Code under the MIT license by Alexander Pruss
#

import lsystem
from mcturtle import *
from sys import argv
COLORS = (WOOL_WHITE,HARDENED_CLAY_STAINED_WHITE,WOOL_PINK,WOOL_MAGENTA,WOOL_PURPLE,HARDENED_CLAY_STAINED_LIGHT_BLUE,HARDENED_CLAY_STAINED_CYAN,HARDENED_CLAY_STAINED_PURPLE,HARDENED_CLAY_STAINED_LIGHT_GRAY,HARDENED_CLAY_STAINED_MAGENTA,HARDENED_CLAY_STAINED_PINK,HARDENED_CLAY_STAINED_RED,WOOL_RED,REDSTONE_BLOCK,HARDENED_CLAY_STAINED_ORANGE,WOOL_ORANGE,HARDENED_CLAY_STAINED_YELLOW,WOOL_YELLOW,WOOL_LIME,HARDENED_CLAY_STAINED_LIME,HARDENED_CLAY_STAINED_GREEN,WOOL_GREEN,HARDENED_CLAY_STAINED_GRAY,WOOL_BROWN,HARDENED_CLAY_STAINED_BROWN,WOOL_GRAY,HARDENED_CLAY_STAINED_BLUE,WOOL_BLUE,WOOL_CYAN,WOOL_LIGHT_BLUE,WOOL_LIGHT_GRAY)
t = Turtle()
t.pendelay(0)
t.turtle(None)
t.penblock(STAINED_GLASS_PURPLE)
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
