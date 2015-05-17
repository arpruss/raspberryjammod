#Martin O'Hanlon
#www.stuffaboutcode.com
#Minecraft Turtle Example - Spiral
import minecraftturtle
import mcpi.minecraft as minecraft
import mcpi.block as block
import random

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)

steve.penblock(block.WOOL.id, 1)
steve.speed(10)
steve.up(5)

for step in range(0,1000):
    steve.forward(2)
    steve.right(10)
