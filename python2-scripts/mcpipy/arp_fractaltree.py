#based on code by Martin O'Hanlon (www.stuffaboutcode.com)
#Minecraft Turtle Example ported to ARP's Turtle class

from turtle import *
import random

def tree(branchLen,t):
    if branchLen > 6:
        t.penblock(Block(WOOL.id, random.randint(0,15)))

        #for performance
        x,y,z = t.position.x, t.position.y, t.position.z
        #draw branch
        t.go(branchLen)

        t.up(20)
        tree(branchLen-2, t)

        t.right(90)
        tree(branchLen-2, t)

        t.left(180)
        tree(branchLen-2, t)

        t.down(40)
        t.right(90)
        tree(branchLen-2, t)

        t.up(20)

        #go back
        #t.backward(branchLen)
        #for performance - rather than going back over every line
        t.goto(x, y, z)


t = Turtle()
t.nofollow()
t.verticalangle(90)
t.pendelay(0)
tree(20, t)
