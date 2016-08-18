#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *
import lsystem

t = Turtle()
t.pendelay(0)
t.turtle(None)
t.penblock(block.BRICK_BLOCK)
# ensure angles are always integral multiples of 90 degrees
t.gridalign()

rules = {'X':'X+YF+', 'Y':'-FX-Y'}

def go():
# draw a wall segment with a door
    t.pendown()
    t.penblock(block.BRICK_BLOCK)
    t.startface()
    for i in range(4):
        t.go(4)
        t.pitch(90)
    t.endface()
    t.penup()
    t.go(2)
    t.pendown()
    t.penblock(block.AIR)
    t.pitch(90)
    t.go(1)
    t.penup()
    t.pitch(180)
    t.go(1)
    t.pitch(90)
    t.go(2)

dictionary = { '+': lambda: t.yaw(90),
               '-': lambda: t.yaw(-90),
               'F': lambda: go() }
lsystem.lsystem('FX', rules, dictionary, 14)
