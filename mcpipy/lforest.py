from __future__ import print_function
#
# Code by Alexander Pruss and under the MIT license
#
# L-system with turtle graphics
#

import lsystem
import random
from mineturtle import *

t = Turtle()
t.pendelay(0)
t.turtle(None)
t.verticalangle(90)

def tree():
    global angle
    global thickness
    global length

    angle = 15
    thickness = 8
    length = 10

    t.pendown()
    t.penblock(block.WOOD)
    rules = {'A': [(0.55,'^f[^^f>>>>>>A]>>>[^^f>>>>>>A]>>>>>[^^f>>>>>>A]'),
                    (0.25,'^f>>[^^f>>>>>>A]>>>[^^f>>>>>>A]')]}

    axiom = 'fA'
    material = block.WOOD

    t.penwidth(thickness)
    t.penblock(material)

    stack = []
    def push():
        global length
        global thickness
        stack.append((length,thickness))
        t.push()
        thickness = thickness * 0.6
        if length == 10:
            length = 9
        elif length == 9:
            length = 8.4
        else:
            length = length * 0.75
        if thickness < 1:
            thickness = 1
        if length <= 1.6:
            t.penblock(block.LEAVES_OAK_PERMANENT)
        t.penwidth(thickness)

    def pop():
        global length
        global thickness
        length,thickness = stack.pop()
        t.pop()

    dictionary = {
        '[': push,
        ']': pop,
        '^': lambda: t.pitch(angle),
        '>': lambda: t.roll(angle),
        'f': lambda: t.go(length)

    }

    lsystem.lsystem(axiom, rules, dictionary, 11)
#tree()

MIN_DISTANCE = 30
MAX_TRIES = 100
SIZE = MIN_DISTANCE * 10
OVALITY = 1.5
cx = t.position.x
cy = t.position.y
cz = t.position.z
tryCount = 0
positions = []

while tryCount < MAX_TRIES:
    x = random.uniform(-1,1)
    z = random.uniform(-1,1)
    if x**2 + z**2 > 1:
        continue
    x = cx + SIZE/2 * x
    z = cz + SIZE/2 * OVALITY * z
    ok = True
    for x0,z0 in positions:
        if (x-x0)**2 + (z-z0)**2 < MIN_DISTANCE**2:
            ok = False
            break
    if not ok:
        tryCount += 1
        continue
    positions.append((x,z))
    tryCount = 0
    t.goto(x,cy,z)
    print(x,cy,z)
    t.push()
    t.roll(random.uniform(0,30))
    tree()
    t.pop()
   
