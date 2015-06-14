#Minecraft Turtle Example
from . import minecraftturtle
from . import mcpi.minecraft as minecraft
from . import mcpi.block as block

def tree(branchLen,t):
    if branchLen > 2:
        t.forward(branchLen)
        t.up(20)
        tree(branchLen-2,t)
        t.down(40)
        tree(branchLen-2,t)
        t.up(20)
        t.backward(branchLen)

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


