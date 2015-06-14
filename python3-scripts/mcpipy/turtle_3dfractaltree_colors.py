#Minecraft Turtle Example
from . import minecraftturtle
from . import mcpi.minecraft as minecraft
from . import mcpi.block as block
import random

def tree(branchLen,t):
    if branchLen > 6:
        t.penblock(block.WOOL.id, random.randint(0,15))
        
        #for performance
        x,y,z = t.position.x, t.position.y, t.position.z
        #draw branch
        t.forward(branchLen)
        
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
        t.setposition(x, y, z)

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)

#point up
steve.setverticalheading(90)

#set speed
steve.speed(0)

#call the tree fractal
tree(20, steve)


