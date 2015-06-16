#Minecraft Turtle Example - Crazy Pattern
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

steve.penblock(block.WOOL.id, 11)
steve.speed(10)

for step in range(0,50):
    steve.forward(50)
    steve.right(123)
