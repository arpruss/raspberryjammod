#Martin O'Hanlon
#www.stuffaboutcode.com
#Minecraft Turtle Example
#Ported from the scratch turtle project in "Adventures in Raspberry Pi"
import minecraftturtle
import mcpi.minecraft as minecraft
import mcpi.block as block

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)
steve.speed(0)
steve.setheading(90)
NumberOfSides = 5
Angle = 360 / NumberOfSides
SideLength = 20
WoolColour = 0

for count in range(24):
    for side in range(NumberOfSides):
        steve.forward(SideLength)
        steve.right(Angle)
    steve.right(15)
    WoolColour += 1
    if WoolColour > 15: WoolColour = 0
    steve.penblock(block.WOOL.id, WoolColour)
    #go 3d
    #steve.sety(steve.position.y + 1)
