from mcturtle import *
import sys
from ast import literal_eval

def parseBlock(s):
    try:
        return literal_eval(s)
    except:
        return globals()[s.upper()]

t = Turtle()
t.pendelay(0)
if len(sys.argv) >= 2:
    radius = int(sys.argv[1])
else:
    radius = 10
if len(sys.argv) >= 3:
    material = parseBlock(sys.argv[2])
else:
    material = GOLD_BLOCK
t.penwidth(2*radius)
t.penblock(material)
t.go(0)
t.pitch(90)
t.penup()
t.go(radius+2)
