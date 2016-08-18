from mineturtle import *
from mcpi.block import Block
import sys

t = Turtle()
t.pendelay(0)
if len(sys.argv) >= 2:
    radius = int(sys.argv[1])
else:
    radius = 10
if len(sys.argv) >= 3:
    material = Block.byName(sys.argv[2])
else:
    material = block.GOLD_BLOCK
t.penwidth(2*radius)
t.penblock(material)
t.go(0)
t.pitch(90)
t.penup()
t.go(radius+2)
