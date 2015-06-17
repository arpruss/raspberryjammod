#
# MIT-licensed code by Alexander Pruss
#
from . import lsystem
from .mcturtle import *
t = Turtle()
t.pendelay(0)
t.turtle(None)
t.gridalign()

# Hilbert curve axiom and production rule by Stan Wagon, Mathematica in Action (chapter 6), W. H. Freeman and Co., 1991
rules = { 'X': '^<XF^<XFX+F^>>XFX&F->>XFX+F>X+>' }

count = 0

def go():
  global count
  # seven segments per basic unit
  if count % 7 == 0:
      t.penblock(Block(WOOL.id, (count/7)%16))
  count += 1
  t.go(4)

dictionary = {
  'F': go,
  '+': lambda: t.yaw(90),
  '-': lambda: t.yaw(-90),
  '^': lambda: t.pitch(90),
  '&': lambda: t.pitch(-90),
  '>': lambda: t.roll(90),
  '<': lambda: t.roll(-90)
  }

lsystem.lsystem('X', rules, dictionary, 3)
