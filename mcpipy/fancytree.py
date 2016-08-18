#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *
import random

def tree(depth,thickness,branchLen):
    if depth <= 0:
        return
    if random.random() < 0.2:
        return
    if branchLen < 4:
        t.penblock(block.LEAVES_OAK_PERMANENT)
    else:
        t.penblock(block.WOOD)
    t.penwidth(thickness)
    t.go(branchLen)
    newThickness = thickness / 2
    if newThickness < 1:
        newThickness = 1
    newBranchLen = branchLen * 0.75
    if branchLen < 1:
        branchLen = 1
    for i in range(4):
        t.pitch(30)
        tree(depth-1,newThickness,newBranchLen)
        t.pitch(-30)
        t.roll(90)
    t.penup()
    t.back(branchLen)
    t.pendown()

t = Turtle()
t.turtle(None)
t.pendelay(0)
t.penup()
t.go(10)
t.verticalangle(90)
t.pendown()
tree(8,8,20)
