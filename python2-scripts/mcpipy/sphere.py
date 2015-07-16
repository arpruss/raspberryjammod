from mcturtle import *
import sys
t = Turtle()
t.pendelay(0)
if len(sys.argv) >= 2:
    radius = int(sys.argv[1])
else:
    radius = 10
if len(sys.argv) >= 3:
    material = eval(sys.argv[2].replace("__","(undefined)"))
else:
    material = GOLD_BLOCK
t.penwidth(2*radius)
t.penblock(material)
t.go(0)
t.pitch(90)
t.penup()
t.go(radius+2)
