#Minecraft Turtle Example - Circle
import minecraftturtle
import mcpi.minecraft as minecraft
import mcpi.block as block

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)
steve.speed(10)
for step in range(0,100):
    steve.right(5)
    steve.forward(2)
    
