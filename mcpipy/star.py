#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *
t = Turtle()
t.penblock(block.GOLD_BLOCK)
t.turtle(GIANT)
t.pendelay(0.01)
for i in range(7):
    t.go(50)
    t.left(180.-180./7)
