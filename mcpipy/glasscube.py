#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *

t = Turtle()
t.turtle(None)
t.pendelay(0)
t.angle(0) # align to grid

def face():
  t.startface()
  for i in range(4):
    t.go(20)
    t.yaw(90)
  t.endface()

t.penblock(block.GLASS)
for i in range(2):
  face()
  t.roll(-90)
  face()
  t.roll(90)
  t.pitch(90)
  face()
  t.pitch(-90)
  t.penup()
  t.go(20)
  t.yaw(90)
  t.go(20)
  t.pitch(90)
  t.go(20)
  t.pitch(-90)
  t.yaw(90)
  t.pitch(-90)
  t.pendown()

