from turtle import *
import random
import sys
sys.setrecursionlimit(10000)

def tree(branchSize,depth):
    if random.random() < 0.30:
        return
    t.penblock(WOOD if branchSize >= 4 else LEAVES)
    t.go(branchSize)
    newSize = branchSize * 0.75
    if depth > 1:
        t.up(20)
        tree(newSize, depth-1)

        t.right(90)
        tree(newSize, depth-1)

        t.left(180)
        tree(newSize, depth-1)

        t.down(40)
        t.right(90)
        tree(newSize, depth-1)
        t.up(20)
    t.penup()
    t.back(branchSize)
    t.pendown()

t = Turtle()
t.nofollow()
t.verticalangle(90)
t.pendelay(0)
t.penblock(WOOD)
tree(15,7)
