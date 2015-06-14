#Martin O'Hanlon
#www.stuffaboutcode.com
#Minecraft Turtle Example
from . import minecraftturtle
from . import mcpi.minecraft as minecraft
from . import mcpi.block as block

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)

steve.speed(0)
steve.penblock(block.WOOL.id, 14)
S = 50
for j in range(0, 20):
    steve.up(j*10)
    steve.forward(S)
    
    steve.left(90)
    steve.down(j*10)
    steve.forward(S)

    steve.left(90)
    steve.down(j*10)
    steve.forward(S)

    steve.left(90)
    steve.up(j*10)
    steve.forward(S)
    steve.left(90)

    steve.left(10)
    S = 0.9*S
