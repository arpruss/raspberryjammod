import lsystem
from mcturtle import *
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

dictionary = {
  'F': lambda: t.go(6),
  '+': lambda: t.yaw(-30),
  '-': lambda: t.yaw(30),
  '[': lambda: t.push(),
  ']': lambda: t.pop()
  }

lsystem.lsystem(axiom, rules, dictionary, 5)
